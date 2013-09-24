import sys
import csv

import numpy as np



if __name__ == '__main__':

    ground_truth = sys.argv[1]
    candidate = sys.argv[2]

    #: loading data also: genfromtxt
    g_frame, g_x1, g_y1, g_x2, g_y2 = np.loadtxt(   ground_truth,
                                                    dtype='i8',
                                                    delimiter=',',
                                                    unpack=True,
                                                    usecols=(0,1,2,3,4),
                                                    )
    # print g_x1

    c_frame, c_x1, c_y1, c_x2, c_y2 = np.loadtxt(   candidate,
                                                    delimiter=',',
                                                    unpack=True,
                                                    usecols=(0,1,2,3,4),
                                                    )

    thresholds = np.arange(0.3, 1.05, 0.05)
    ovMax = np.c_[thresholds, np.zeros(np.size(thresholds)), np.zeros(np.size(thresholds))]

    g_check = np.zeros(g_frame, int)
    c_check = np.zeros(c_frame, int)

    for thresh_ind in np.arange(np.size(thresholds)):
        for c_ind in np.arange(np.size(c_frame)):
            for g_ind in np.where(g_frame == c_frame[c_ind]):
                if g_check[g_ind] == 0 and c_check[c_ind] == 0:
                    common_area = np.array([max(g_x1[g_ind], c_x1[c_ind]),
                                            max(g_y1[g_ind], c_y1[c_ind]),
                                            min(g_x2[g_ind], c_x2[c_ind]),
                                            min(g_y2[g_ind], c_y2[c_ind])])
                    common_w = common_area(2) - common_area(0) + 1
                    common_h = common_area(3) - common_area(1) + 1

                    if common_w > 0 and common_h > 0:
                        u_area =    (g_x2[g_ind] - g_x1[g_ind]) * (g_y2[g_ind] - g_y1[g_ind])
                                +   (c_x2[c_ind] - c_x1[c_ind]) * (c_y2[c_ind] - c_y1[c_ind])
                                -   common_w * common_h

                        ov = (common_w * common_h) / u_area
                        if ov > thresholds[thresh_ind]:
                            g_check[g_ind] = 1
                            c_check[c_ind] = 1
        tp = np.size(g_check[g_check == 1])
        fn = np.size(g_check[g_check == 0])
        fp = np.size(c_check[c_check == 0])

        ovMax[thresh_ind, 1] = tp / (fp + tp)
        ovMax[thresh_ind, 2] = tp / np.size(g_frame)
    s_tmp = candidate.split('.')
    np.savetxt(s_tmp[0]+'_evals'+s_tmp[1], ovMax, delimiter=',')