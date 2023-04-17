"""
This module is a plugin for projection on pyHiM.
"""

import json
import pathlib
from typing import TYPE_CHECKING
from napari.layers import Layer, Image
from napari.types import LayerDataTuple
from magicgui import magic_factory
from magicgui.widgets import FunctionGui
import numpy as np
import scipy.optimize as spo
from apifish.stack import projection

if TYPE_CHECKING:
    import napari

    #####################################################################
    #####################################################################
    ######################## Adapted from pyHiM #########################
    #####################################################################
    #####################################################################


def calculate_zrange(idata, z_min, z_max, window_security, z_windows):
    """
    Calculates the focal planes based max standard deviation
    """
    num_planes = z_max - z_min
    std_matrix = np.zeros(num_planes)
    mean_matrix = np.zeros(num_planes)

    # calculate STD in each plane
    for i in range(0, num_planes):
        std_matrix[i] = np.std(idata[i])
        mean_matrix[i] = np.mean(idata[i])

    max_std = np.max(std_matrix)
    i_focus_plane = np.where(std_matrix == max_std)[0][0]
    # Select a window to avoid being on the edges of the stack

    if i_focus_plane < window_security or (
        i_focus_plane > num_planes - window_security
    ):
        focus_plane = i_focus_plane
    else:
        # interpolate zfocus
        axis_z = range(
            max(
                z_min,
                i_focus_plane - window_security,
                min(
                    z_max,
                    i_focus_plane + window_security,
                ),
            )
        )

        std_matrix -= np.min(std_matrix)
        std_matrix /= np.max(std_matrix)

        try:
            fitgauss = spo.curve_fit(
                gaussian, axis_z, std_matrix[axis_z[0] : axis_z[-1] + 1]
            )
            focus_plane = int(fitgauss[0][1])
        except RuntimeError:
            print("Warning, too many iterations")
            focus_plane = i_focus_plane

    zmin = max(
        window_security,
        focus_plane - z_windows,
    )
    zmax = min(
        num_planes,
        window_security + num_planes,
        focus_plane + z_windows,
    )
    zrange = range(zmin, zmax + 1)

    return focus_plane, zrange


def reinterpolate_focal_plane(data, block_size=128, z_windows=0):
    focal_plane_matrix, z_range, block = projection.reinterpolate_focal_plane(
        data, block_size_xy=block_size, window=z_windows
    )
    # reassembles image
    output = projection.reassemble_images(
        focal_plane_matrix, block, window=z_windows
    )
    return output, focal_plane_matrix, z_range

def project_image_2d(img, z_range, mode):
    # sums images
    i_collapsed = None
    if "MIP" in mode:
        # Max projection of selected planes
        i_collapsed = projection.maximum_projection(img[z_range[1][0] : z_range[1][-1]])
    elif "sum" in mode:
        # Sums selected planes
        i_collapsed = projection.sum_projection(img[z_range[1][0] : (z_range[1][-1] + 1)])
    else:
        print(f"ERROR: mode not recognized. Expected: MIP or sum. Read: {mode}")
    return i_collapsed

    #####################################################################
    #####################################################################
    #####################################################################
    #####################################################################


operation_dict = {
    "z-project sum": lambda x: np.sum(x, axis=2),
    "z-project mean": lambda x: np.mean(x, axis=2),
    "z-project max": lambda x: np.max(x, axis=2),
}


def _mode_choices(wdg):
    # Update operations
    opts = ["full", "manual", "automatic", "laplacian"]
    return opts


def on_init(widget: FunctionGui):
    """called each time widget_factory creates a new widget."""

    @widget.save.changed.connect
    def on_save_changed(save_val: bool):
        if save_val:
            widget.save_path.visible = True
        else:
            widget.save_path.visible = False

    @widget.layer0.changed.connect
    def on_layer_changed(lyr: Layer):
        widget.z_max.max = lyr.data.shape[0]

    @widget.z_max.changed.connect
    def on_layer_changed(lyr: Layer):
        widget.z_min.max = widget.z_max.value - 1

    @widget.z_min.changed.connect
    def on_layer_changed(lyr: Layer):
        widget.z_max.min = widget.z_min.value + 1


@magic_factory(
    widget_init=on_init,
    mode={"choices": _mode_choices},
    call_button="Project",
    save={
        "widget_type": "CheckBox",
        "value": False,
        "name": "save",
        "text": "Save configuration",
    },
    save_path={"mode": "d", "visible": False},
    z_project_option={"choices": ["sum", "MIP"]},
    block_size={"choices": [32, 64, 128, 256, 512, 1024], "value": 256},
    z_min={"widget_type": "Slider", "min": 0, "max": 0, "value": 0},
    z_max={"widget_type": "Slider", "min": 1, "max": 1, "value": 1},
)
def do_projection(
    layer0: Layer,
    mode: str,
    block_size: int,
    z_min: int,
    z_max: int,
    z_windows: int,
    window_security: int,
    z_project_option: str,
    save: bool,
    save_path: pathlib.Path,
) -> LayerDataTuple:

    # Store source images in metadata
    layer0_name = (
        layer0._source.path if layer0._source.path is not None else layer0.name
    )

    # Apply operationTODO
    # data = operationTODO_dict.get(operationTODO)(layer0.data.T).T

    #############################################################################################
    #############################################################################################
    #############################################################################################

    if mode == "automatic":
        print("> Calculating planes automaticly...")
        z_range = calculate_zrange(
            layer0.data, z_min, z_max, window_security, z_windows
        )

    elif mode == "full":
        z_range = (round((z_min + z_max) / 2), range(z_min, z_max))

    if mode == "laplacian":
        print("Stacking using Laplacian variance...")
        (
            data_2d,
            focal_plane_matrix,
            z_range,
        ) = reinterpolate_focal_plane(layer0.data, block_size=128, z_windows=0)
        focus_plane = z_range[0]

    else:
        # Manual: reads from parameters file
        if z_min >= z_max:
            raise SystemExit(
                "zmin is equal or larger than zmax in configuration file. Cannot proceed."
            )
        z_range = (round((z_min + z_max) / 2), range(z_min, z_max))

    if mode != "laplacian":
        data_2d = project_image_2d(
            layer0.data,
            z_range,
            z_project_option,
        )
        focus_plane = z_range[0]
        z_range = z_range[1]

    #############################################################################################
    #############################################################################################
    #############################################################################################

    # if save:
    #     data_to_print = {"operationTODO": operationTODO, "image": layer0_name}
    #     with open("json_data_todelete.json", "w") as outfile:
    #         json.dump(data_to_print, outfile)
    #     print("Configuration save as json file")

    return [(data_2d, {"name": mode + z_project_option}, layer0._type_string)]
