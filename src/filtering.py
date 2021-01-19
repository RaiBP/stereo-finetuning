import cv2
import numpy as np


def filtering(left_matcher, left, right, lmbda=8000, sigma=1.0):
    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

    left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

    left_disp = left_matcher.compute(left, right)
    right_disp = right_matcher.compute(left, right)

    displ = np.int16(left_disp)
    dispr = np.int16(right_disp)

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(left_matcher)
    wls_filter.setLambda(lmbda)
    wls_filter.setSigmaColor(sigma)
    filtered_disp = wls_filter.filter(displ, left, disparity_map_right=dispr)

    return (filtered_disp * 1 / 16.0).astype(np.uint8), wls_filter.getROI()
