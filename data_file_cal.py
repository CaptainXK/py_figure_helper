def cal_one_file(file_path):
    file = open(file_path, mode='r')
    lines = file.readlines()
    val = ''
    
    res = 0
    for val in lines:
        res += int(val)

    return float(res) / len(lines)

def create_fig(plt, xlist, ylists, xlable, ylabel, title, labels, tar_file):
    #refresh plt
    plt.figure(figsize=(6, 4))

    #get max y value
    y_max = max(ylists[0])
    if y_max <= max(ylists[1]):
        y_max = max(ylists[1])

    plt.ylim(0, y_max + (y_max / 10))

    #create
    plt.title(title)
    plt.xlabel(xlable)
    plt.ylabel(ylabel)

    #draw
    # line_style=['-.', ':', '--', '-']
    markers=['o','^','v']
    for (cur_ylist, cur_label, cur_marker) in zip(ylists, labels, markers):
        plt.plot(xlist, cur_ylist, label=cur_label, linestyle='-', marker=cur_marker, markerfacecolor='none')
    # plt.plot(xlist, ylists[0], label=labels[0])
    # plt.plot(xlist, ylists[1], label=labels[1])

    plt.legend()#print the label for each data line

    # plt.show()

    plt.savefig(tar_file)

    print(tar_file + " had been created")
