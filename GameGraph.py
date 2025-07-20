import json
import matplotlib.pyplot as plt
import os




# Load color data from JSON file
with open('TeamSettings.json', 'r') as file:
    data = json.load(file)
    colors = data['colors']  # List of RGB lists (e.g., [[0,0,255], ...])

# Convert JSON colors to normalized RGBA tuples (with alpha=0.75)
colorArr = [
    (r/255.0, g/255.0, b/255.0, 0.75)
    for r, g, b in colors
]

os.chdir("Game Data")

def plot_population(file_path, axis, title):
    with open(file_path) as file:
        data = json.load(file)
    team_no = len(data[0])
    for team in range(team_no):
        array_x = [data[j][team] for j in range(len(data))]
        array_y = list(range(len(data)))
        axis.plot(array_y, array_x, c=colorArr[team])
    axis.set_ylabel(title)

def plot_scatter(file_path1, file_path2, axis, xlabel, ylabel, dots=False):
    with open(file_path1) as file1, open(file_path2) as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)
    team_no = len(data1[0])
    for team in range(team_no):
        array_x = [data1[j][team] for j in range(len(data1))]
        array_y = [data2[j][team] for j in range(len(data2))]
        if dots:
            axis.plot(array_x, array_y, "o" , c=colorArr[team])
        else:
            axis.plot(array_x, array_y, c=colorArr[team])
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)

def plot_over_time(file_path, axis, ylabel):
    with open(file_path) as file:
        data = json.load(file)
    team_no = len(data[0])
    for team in range(team_no):
        array = [data[i][team] for i in range(len(data))]
        normal_array = list(range(len(data)))
        axis.plot(normal_array, array, c=colorArr[team])
    axis.set_ylabel(ylabel)
    axis.set_xlabel("Time (ticks)")


def plot_ratio(file_path1, file_path2, axis, ylabel):
    with open(file_path1) as file1, open(file_path2) as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)
    team_no = len(data1[0])
    for team in range(team_no):
        ratio_array = [
            (data1[i][team] / data2[i][team]) if data2[i][team] != 0 else 0
            for i in range(len(data1))
        ]
        ticks = list(range(len(data1)))
        axis.plot(ticks, ratio_array, c=colorArr[team])
    axis.set_ylabel(ylabel)
    axis.set_xlabel("Time (ticks)")


def plot_ratio_against_x(numerator_file, denominator_file, x_file, axis, xlabel, ylabel, dots=False):
    with open(numerator_file) as file1, open(denominator_file) as file2, open(x_file) as file3:
        data1 = json.load(file1)
        data2 = json.load(file2)
        data_x = json.load(file3)
    
    team_no = len(data1[0])
    for team in range(team_no):
        ratio_array = [
            (data1[i][team] / data2[i][team]) if data2[i][team] != 0 else 0
            for i in range(len(data1))
        ]
        x_array = [data_x[i][team] for i in range(len(data_x))]
        
        if dots:
            axis.plot(x_array, ratio_array, "o", c=colorArr[team])
        else:
            axis.plot(x_array, ratio_array, c=colorArr[team])
    
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)




# Population plots
fig, axs = plt.subplots(3, 4)
plot_population("TankPop.json", axs[0, 0], "Tank Population")
plot_population("FortPop.json", axs[0, 1], "Fort Population")
plot_over_time("AverageTankAge.json", axs[2, 0], "Average Tank Age (ms)")
plot_over_time("Territory.json", axs[2, 1], "Territory Tiles")
plot_over_time("TanksKilled.json", axs[1, 0], "Tanks Killed")
plot_over_time("TanksLost.json", axs[1, 1], "Tanks Lost")

plot_population("CapturedFortPop.json", axs[0, 2], "Captured Forts")
plot_population("SpecialTankPop.json", axs[1, 2], "Special Tank Population")
plot_population("SpecialFortPop.json", axs[2, 2], "Special Fort Population")

plot_over_time("CapturedFortRatio.json", axs[0, 3], "Captured Fort Ratio")
plot_over_time("SpecialTankRatio.json", axs[1, 3], "Special Tank Ratio")
plot_over_time("SpecialFortRatio.json", axs[2, 3], "Spectial Fort Ratio")
plt.show()

# Scatter plot for Tanks Killed/Lost
fig, ax = plt.subplots(1)
plot_scatter("TanksLost.json", "TanksKilled.json", ax, "Tanks Lost", "Tanks Killed")
plt.show()

fig, ax = plt.subplots(1)
plot_scatter("SpecialTankRatio.json", "AverageTankAge.json", ax, "Special Tank Ratio", "Average Tank Age", True)
plt.show()

fig, ax = plt.subplots(1)
plot_scatter("TankPop.json", "FortPop.json", ax, "Tanks", "Forts", True)
plt.show()

fig, ax = plt.subplots(2,2)
plot_scatter("CapturedFortRatio.json", "SpecialFortRatio.json", ax[0,0], "Assimilating Forts Ratio", "Special Forts Ratio", True)
plot_ratio("Territory.json", "FortPop.json", ax[0,1], "Territory - Fort Population ratio")
plot_scatter("SpecialFortRatio.json", "SpecialTankRatio.json", ax[1,0], "Special Forts Ratio", "Special Tanks Ratio", True)
plot_ratio_against_x("Territory.json", "FortPop.json", "AverageTankAge.json", ax[1,1], "Average Tank Age", "Territory - Fort Population ratio", True)
plt.show()

