import cv2


def generate_stereo_sgbm_disparity_map(left_img, right_img, min_disp=0, num_disp=64, block_size=5, p1=0, p2=0,
                                       prefilter_cap=1, disp12maxdiff=-1, uniqueness_ratio=0, speckle_windows_size=0,
                                       speckle_range=0, use_dynamic_programming=False):
    """

    :param use_dynamic_programming:
    :param prefilter_cap:
    :param left_img:
    :param right_img:
    :param min_disp:
    :param num_disp:
    :param block_size:
    :param p1:
    :param p2:
    :param disp12maxdiff:
    :param uniqueness_ratio:
    :param speckle_windows_size:
    :param speckle_range:
    :return:
    """
    mode = cv2.StereoSGBM_MODE_HH if use_dynamic_programming else cv2.StereoSGBM_MODE_SGBM

    stereo = cv2.StereoSGBM_create(minDisparity=min_disp,
                                   numDisparities=num_disp,
                                   blockSize=block_size,
                                   P1=p1,
                                   P2=p2,
                                   preFilterCap=prefilter_cap,
                                   disp12MaxDiff=disp12maxdiff,
                                   uniquenessRatio=uniqueness_ratio,
                                   speckleWindowSize=speckle_windows_size,
                                   speckleRange=speckle_range,
                                   mode=mode)

    print("\nComputing the disparity  map...")
    disparity_map = stereo.compute(left_img, right_img)

    return disparity_map


def generate_stereo_bm_disparity_map(left_img, right_img, min_disp=0, num_disp=64, block_size=5, prefilter_cap=1, disp12maxdiff=-1, uniqueness_ratio=0, speckle_windows_size=0,
                                     speckle_range=0, prefilter_size=5, texture_threshold=0,
                                     use_xsobel=False):
    """

    :param left_img:
    :param right_img:
    :param min_disp:
    :param num_disp:
    :param block_size:
    :param prefilter_cap:
    :param disp12maxdiff:
    :param uniqueness_ratio:
    :param speckle_windows_size:
    :param speckle_range:
    :param prefilter_size:
    :param texture_threshold:
    :param use_xsobel:
    :return:
    """
    prefilter_type = cv2.STEREO_BM_PREFILTER_XSOBEL if use_xsobel else cv2.STEREO_BM_PREFILTER_NORMALIZED_RESPONSE

    stereo = cv2.StereoBM_create(numDisparities=num_disp, blockSize=block_size)
    stereo.setPreFilterCap(prefilter_cap)
    stereo.setMinDisparity(min_disp)
    stereo.setDisp12MaxDiff(disp12maxdiff)
    stereo.setUniquenessRatio(uniqueness_ratio)
    stereo.setSpeckleWindowSize(speckle_windows_size)
    stereo.setSpeckleRange(speckle_range)
    stereo.setPreFilterSize(prefilter_size)
    stereo.setTextureThreshold(texture_threshold)
    stereo.setPreFilterType(prefilter_type)

    print("\nComputing the disparity  map...")
    disparity_map = stereo.compute(left_img, right_img)

    return disparity_map
