"""
This module is for json parameters.
"""

import json


DEFAULT_PARAM = {
    "common": {
        "acquisition": {
            "positionROIinformation": 3,
            "fileNameRegExp": "scan_(?P<runNumber>[0-9]+)_(?P<cycle>[\\w|-]+)_(?P<roi>[0-9]+)_ROI_converted_decon_(?P<channel>[\\w|-]+).tif",
            "DAPI_channel": "ch00",
            "fiducialDAPI_channel": "ch01",
            "RNA_channel": "ch02",
            "fiducialBarcode_channel": "ch00",
            "fiducialMask_channel": "ch00",
            "barcode_channel": "ch01",
            "mask_channel": "ch01",
            "label_channel": "ch00",  # in future this field will contain the ch for the label. This parameter will supersed the individual channel fields above.
            "label_channel_fiducial": "ch01",  # in future this field will contain the ch for the label fiducial. This parameter will supersed the individual channel fields above.
            "pixelSizeXY": 0.1,
            "zBinning": 2,
            "parallelizePlanes": False,  # if True it will parallelize inner loops (plane by plane). Otherwise outer loops (e.g. file by file)
            "pixelSizeZ": 0.25,
        },  # barcode, fiducial
        "zProject": {
            "folder": "zProject",  # output folder
            "operation": "skip",  # overwrite, skip
            "mode": "full",  # full, manual, automatic, laplacian
            "blockSize": 256,
            "display": True,
            "saveImage": True,
            "zmin": 1,
            "zmax": 59,
            "zwindows": 15,
            "windowSecurity": 2,
            "zProjectOption": "MIP",  # sum or MIP
        },
        "alignImages": {
            "folder": "alignImages",  # output folder
            "operation": "overwrite",  # overwrite, skip
            "outputFile": "alignImages",
            "referenceFiducial": "RT27",
            "localAlignment": "block3D",  # options: None, mask2D, block3D
            "alignByBlock": True,  # alignByBlock True will perform block alignment
            "tolerance": 0.1,  # Used in blockAlignment to determine the % of error tolerated
            "lower_threshold": 0.999,  # lower threshold to adjust image intensity levels before xcorrelation for alignment in 2D
            "higher_threshold": 0.9999999,  # higher threshold to adjust image intensity levels before xcorrelation for alignment in 2D
            "3D_lower_threshold": 0.9,  # lower threshold to adjust image intensity levels before xcorrelation for Alignment3D
            "3D_higher_threshold": 0.9999,  # higher threshold to adjust image intensity levels before xcorrelation for Alignment3D
            "background_sigma": 3.0,  # used to remove inhom background
            "localShiftTolerance": 1,
            "blockSize": 256,
        },
        "buildsPWDmatrix": {
            "folder": "buildsPWDmatrix",  # output folder
            "tracing_method": [
                "masking",
                "clustering",
            ],  # available methods: masking, clustering
            "mask_expansion": 8,  # Expands masks until they collide by a max of 'mask_expansion' pixels
            "flux_min": 10,  # min flux to keeep object
            "flux_min_3D": 0.1,  # min flux to keeep object
            "kd_tree_distance_threshold_mum": 1,  # distance threshold used to build KDtree
            "colormaps": {
                "PWD_KDE": "terrain",
                "PWD_median": "terrain",
                "contact": "coolwarm",
                "Nmatrix": "Blues",
            },  # colormaps used for plotting matrices
            "toleranceDrift": 1,  # tolerance used for block drift correction, in px
            "remove_uncorrected_localizations": True,  # if True it will removed uncorrected localizations, otherwise they will remain uncorrectd.
        },
        "segmentedObjects": {
            "folder": "segmentedObjects",  # output folder
            "operation": "2D,3D",  # options: 2D or 3D
            "outputFile": "segmentedObjects",
            "Segment3D": "overwrite",
            "background_method": "inhomogeneous",  # flat or inhomogeneous or stardist
            "stardist_basename": "/mnt/grey/DATA/users/marcnol/pyHiM_AI_models/networks",
            "stardist_network": "stardist_nc14_nrays:64_epochs:40_grid:2",  # network for 2D barcode segmentation
            "stardist_network3D": "stardist_nc14_nrays:64_epochs:40_grid:2",  # network for 3D barcode segmentation
            "tesselation": True,  # tesselates masks
            "background_sigma": 3.0,  # used to remove inhom background
            "threshold_over_std": 1.0,  # threshold used to detect sources
            "fwhm": 3.0,  # source size in px
            "brightest": 1100,  # max number of sources segmented per FOV
            "intensity_min": 0,  # min int to keep object
            "intensity_max": 59,  # max int to keeep object
            "area_min": 50,  # min area to keeep object
            "area_max": 500,  # max area to keeep object
            "3Dmethod": "thresholding",  # options: 'thresholding' or 'stardist', 'zASTROPY', 'zProfile'
            "residual_max": 2.5,  # z-profile Fit: max residuals to keeep object
            "sigma_max": 5,  # z-profile Fit: max sigma 3D fitting to keeep object
            "centroidDifference_max": 5,  # z-profile Fit: max diff between Moment and z-gaussian fits to keeep object
            "3DGaussianfitWindow": 3,  # z-profile Fit: window size to extract subVolume, px. 3 means subvolume will be 7x7.
            "3dAP_window": 5,  # constructs a YZ image by summing from xPlane-window:xPlane+window
            "3dAP_flux_min": 2,  # # threshold to keep a source detected in YZ
            "3dAP_brightest": 100,  # number of sources sought in each YZ plane
            "3dAP_distTolerance": 1,  # px dist to attribute a source localized in YZ to one localized in XY
            "3D_threshold_over_std": 5,
            "3D_sigma": 3,
            "3D_boxSize": 32,
            "3D_filter_size": 3,
            "3D_area_min": 10,
            "3D_area_max": 250,
            "3D_nlevels": 64,
            "3D_contrast": 0.001,
            "3D_psf_z": 500,
            "3D_psf_yx": 200,
            "3D_lower_threshold": 0.99,
            "3D_higher_threshold": 0.9999,
            "reducePlanes": True,  # if true it will calculate focal plane and only use a region around it for segmentSources3D, otherwise will use the full stack
        },
    },
    "labels": {
        "fiducial": {"order": 1},
        "barcode": {"order": 2},
        "DAPI": {"order": 3},
        "mask": {"order": 5},
        "RNA": {"order": 4},
    },
}


def update_zproject(
    mode: str,
    block_size: int,
    z_min: int,
    z_max: int,
    z_windows: int,
    window_security: int,
    z_project_option: str,
):
    new_dic = DEFAULT_PARAM.copy()
    new_dic["common"]["zProject"]["mode"] = mode
    new_dic["common"]["zProject"]["blockSize"] = block_size
    new_dic["common"]["zProject"]["zmin"] = z_min
    new_dic["common"]["zProject"]["zmax"] = z_max
    new_dic["common"]["zProject"]["zwindows"] = z_windows
    new_dic["common"]["zProject"]["windowSecurity"] = window_security
    new_dic["common"]["zProject"]["zProjectOption"] = z_project_option

    return new_dic
