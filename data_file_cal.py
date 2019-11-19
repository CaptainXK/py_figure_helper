def cal_one_file(file_path):
    file = open(file_path, mode='r')
    lines = file.readlines()
    val = ''
    
    res = 0
    for val in lines:
        res += int(val.replace('\n',''))

    return float(res) / len(lines)

def create_fig(plt, xlist, ylists, xlable, ylabel, title, labels, tar_file, type):
    #refresh plt
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)

    #get max y value
    y_max = max(ylists[0])
    if y_max <= max(ylists[1]):
        y_max = max(ylists[1])

    plt.ylim(0, y_max + (y_max / 3))

    #create
    plt.title(title)
    plt.xlabel(xlable)
    plt.ylabel(ylabel)

    #draw
    # line_style=['-.', ':', '--', '-']
    if type == 'plot':
        markers=['o','^','v']
        for (cur_ylist, cur_label, cur_marker) in zip(ylists, labels, markers):
            plt.plot(xlist, cur_ylist, label=cur_label, linestyle='-', marker=cur_marker, markerfacecolor='none')
        # plt.plot(xlist, ylists[0], label=labels[0])
        # plt.plot(xlist, ylists[1], label=labels[1])
    else:
        tot_width, n = 0.9,3
        _width = tot_width / n
        patterns = ['///','+++','xxx']
        offsets = [-1, 0, 1]
        cur_xlist = list(range(len(xlist)))
        for (cur_ylist, cur_label, pattern, offset) in zip(ylists, labels, patterns, offsets):
            # set offset of each bar
            for x in range(len(xlist)):
                cur_xlist[x] = xlist[x] + offset * _width
            plt.bar(cur_xlist, cur_ylist, width=_width, label=cur_label, hatch=pattern)
        
        # set ticks and labels of x-axis
        xlabels = []
        for i in range(6):
            xlabels.append("reddit_{}".format(i))
        ax.set_xticks(range(6))
        ax.set_xticklabels(xlabels)
        
    plt.legend()#print the label for each data line

    # plt.show()

    plt.savefig("{}/{}".format("figures", tar_file))

    print(tar_file + " had been created")
