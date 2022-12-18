import matplotlib.pyplot as plt
import numpy as np

import json

if __name__ == '__main__':
    with open('5x5.txt','r') as f:
        lines = f.readlines()
    x = np.linspace(1, 100, 100)
    data_1 = json.loads(lines[1])
    data_2 = json.loads(lines[3])
    data_3 = json.loads(lines[5])
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('5x5')
    ax1.hist(data_1,label = "baseline_ai")
    ax1.hist(data_2,label = "a_star_ai")
    ax1.legend()
    ax2.hist(data_3,label = "a_star_ai node_count")
    ax2.legend()
    plt.show()
