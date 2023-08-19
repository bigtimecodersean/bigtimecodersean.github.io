import matplotlib.pyplot as plt
import numpy as np


def plot_qs(qs_for_agent, num_agents):
    oldnum = len(list(qs_for_agent.values())[0])

    myarray = []
    iterat = 0
    for idx, item in qs_for_agent.items():

        iterat += 1
        item = item.reshape(item.shape[0], 1)
        newnum = len(item)

        if newnum == oldnum:
            myarray.append(item)

        if newnum != oldnum or iterat == len(qs_for_agent) - 1:

            print(f"Shape of qs for this number of agents so far: {np.array(myarray).shape}")
            if len(myarray) > 0:
                if iterat > 100:
                    plt.imshow(np.array(myarray), cmap="gray", aspect=0.05)
                    plt.yticks(
                        list(range(0, 0 + np.array(myarray).shape[0]))[::50],
                        labels=list(range(idx - np.array(myarray).shape[0], idx))[::50],
                    )

                else:
                    plt.imshow(np.array(myarray), cmap="gray")
                    plt.yticks(
                        list(range(0, 0 + np.array(myarray).shape[0]))[::2],
                        labels=list(range(idx - np.array(myarray).shape[0], idx))[::2],
                    )

                plt.title(f"QS for Num agents: {num_agents[idx]}, Num states: {oldnum}")
                # plt.yticklabels(list(range(idx, idx +np.array(myarray).shape[0]))[::2])

                if oldnum > 8:
                    plt.xticks(list(range(oldnum))[::4])
                else:
                    plt.xticks(range(oldnum))
                plt.xlabel("States")
                plt.ylabel("Time")
                plt.show()
            else:
                print(myarray)
            myarray = [item]

        oldnum = newnum


def plot_qpi(qpi_for_agent, num_agents):
    oldnum = len(list(qpi_for_agent.values())[0])

    myarray = []
    for idx, item in qpi_for_agent.items():
        item = item.reshape(item.shape[0], 1)
        newnum = len(item)
        if newnum == oldnum:
            myarray.append(item)

        if newnum != oldnum or idx == len(qpi_for_agent) - 1:

            print(f"Shape of qpi for this number of agents so far: {np.array(myarray).shape}")
            if len(myarray) > 0:
                if idx > 100:
                    plt.imshow(np.array(myarray), cmap="gray", aspect=0.05)
                    plt.yticks(
                        list(range(0, 0 + np.array(myarray).shape[0]))[::10],
                        labels=list(range(idx - np.array(myarray).shape[0], idx))[::10],
                    )

                else:
                    plt.imshow(np.array(myarray), cmap="gray")
                    plt.yticks(
                        list(range(0, 0 + np.array(myarray).shape[0]))[::2],
                        labels=list(range(idx - np.array(myarray).shape[0], idx))[::2],
                    )

                plt.title(f"Q_pi for Num agents: {num_agents[idx]}, Num states: {oldnum}")
                # plt.yticklabels(list(range(idx, idx +np.array(myarray).shape[0]))[::2])

                if oldnum > 8:
                    plt.xticks(list(range(oldnum))[::4])
                else:
                    plt.xticks(range(oldnum))
                plt.xlabel("Actions")
                plt.ylabel("Time")
                plt.show()
            myarray = [item]

        oldnum = newnum


def plot_efe(qpi_for_agent, num_agents):
    oldnum = len(list(qpi_for_agent.values())[0])

    myarray = []
    for idx, item in qpi_for_agent.items():
        item = item.reshape(item.shape[0], 1)
        newnum = len(item)
        if newnum == oldnum:
            myarray.append(item)

        if newnum != oldnum or idx == len(qpi_for_agent) - 1:

            print(f"Shape of efe for this number of agents so far: {np.array(myarray).shape}")
            if len(myarray) > 0:
                if idx > 100:
                    plt.imshow(np.array(myarray), cmap="gray", aspect=0.05)
                    plt.yticks(
                        list(range(0, 0 + np.array(myarray).shape[0]))[::10],
                        labels=list(range(idx - np.array(myarray).shape[0], idx))[::10],
                    )

                else:
                    plt.imshow(np.array(myarray), cmap="gray")
                    plt.yticks(
                        list(range(0, 0 + np.array(myarray).shape[0]))[::2],
                        labels=list(range(idx - np.array(myarray).shape[0], idx))[::2],
                    )

                plt.colorbar()
                plt.title(f"EFE for Num agents: {num_agents[idx]}, Num states: {oldnum}")
                # plt.yticklabels(list(range(idx, idx +np.array(myarray).shape[0]))[::2])

                if oldnum > 8:
                    plt.xticks(list(range(oldnum))[::4])
                else:
                    plt.xticks(range(oldnum))
                plt.xlabel("Actions")
                plt.ylabel("Time")
                plt.show()
                print(idx)
            myarray = [item]

        oldnum = newnum


def plot_num_agents(num_agents):

    plt.plot(list(num_agents.keys()), list(num_agents.values()))
    plt.xlabel("Time")
    plt.ylabel("Number of agents")


def plot_obs(all_obs, num_states):
    fig, ax = plt.subplots(2, 2, figsize=(10, 10))

    ax[0][0].plot(list(all_obs[0].keys()), list(all_obs[0].values()))
    ax[0][0].set_title("Agent 1")
    ax[0][0].set_ylabel("Observations")
    ax[0][0].set_xlabel("Time")

    ax[0][0].plot(
        list(all_obs[0].keys()),
        num_states[: len(list(all_obs[0].keys()))],
        label="Number of states",
    )

    ax[0][1].plot(list(all_obs[1].keys()), list(all_obs[1].values()))
    ax[0][1].set_title("Agent 2")
    ax[0][1].set_ylabel("Observations")
    ax[0][1].set_xlabel("Time")
    ax[0][1].plot(
        list(all_obs[1].keys()),
        num_states[: len(list(all_obs[1].keys()))],
        label="Number of states",
    )

    ax[1][0].plot(list(all_obs[2].keys()), list(all_obs[2].values()))
    ax[1][0].set_title("Agent 3")
    ax[1][0].set_ylabel("Observations")
    ax[1][0].set_xlabel("Time")
    ax[1][0].plot(all_obs[2].keys(), num_states[: len(all_obs[2].keys())], label="Number of states")

    ax[1][1].plot(list(all_obs[3].keys()), list(all_obs[3].values()))
    ax[1][1].set_title("Agent 4")
    ax[1][1].set_ylabel("Observations")
    ax[1][1].set_xlabel("Time")
    ax[1][1].plot(all_obs[3].keys(), num_states[: len(all_obs[3].keys())], label="Number of states")


def plot_C(qs_for_agent, num_agents, num_states):
    oldnum = len(list(qs_for_agent.values())[0])

    myarray = []
    iterat = 0
    for idx, item in qs_for_agent.items():
        item = item[0]

        iterat += 1
        item = item.reshape(item.shape[0], 1)
        newnum = len(item)

        if newnum == oldnum:
            myarray.append(item)

        if newnum != oldnum or iterat == len(qs_for_agent) - 1:

            print(f"Shape of C for this number of agents so far: {np.array(myarray).shape}")
            if len(myarray) > 0:
                if iterat > 100:
                    plt.imshow(np.array(myarray).T[:, :, 0], cmap="gray")
                    plt.xticks(range(8), labels=range(8))

                else:
                    plt.imshow(np.array(myarray).T[:, :, 0], cmap="gray")
                    plt.xticks(range(8), labels=range(8))

                plt.title(f"C for Num agents: {num_agents[idx]}, Num states: {num_states[idx]}")

                plt.ylabel("Prior")
                plt.xlabel("Observations")
                plt.show()
            else:
                print(myarray)
            myarray = [item]

        oldnum = newnum
