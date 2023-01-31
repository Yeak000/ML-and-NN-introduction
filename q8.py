import pandas as pd
import numpy as np
from maze_env_1 import Maze
from q_learning_model_maze import *


def update(q_table = None):
    s_len = []
    min_s = []
    min_len_s = 99999
    if q_table is None:
        n = 10000
    else:
        n = 10
    for episode in range(n):
        if RL.q_table_True == 0:
            if episode <= 500:
                RL.e_greedy = 0.0008*episode+0.59
            else:
                RL.e_greedy = 0.99
        else:
            RL.e_greedy = 1
        s = env.reset()

        while True:
            env.render()

            # 选择一个动作
            action = RL.choose_action(str(s))
            o_s = s.copy()

            # 执行这个动作得到反馈（下一个状态s 奖励r 是否结束done）
            s_, r, done = env.step(action)

            # 更新状态表
            RL.rl(str(s), action, r, str(s_))
            #
            # if r == -100:
            #     s = o_s
            # else:
            #     s = s_
            s = s_

            if done:
                t = len(env.old_s)
                s_len.append(t)
                if t < min_len_s:
                    min_len_s = t
                    min_s = env.old_s
                break
    return min_len_s,min_s

def s_to_road(s_list):
    road_list = []
    for i in s_list:
        road_list.append([int(((i[0]+i[2])/2-8)/16),int(((i[1]+i[3])/2-8)/16)])
    return road_list


if __name__ == "__main__":
    end = [29, 35]

    endx = end[0]
    endy = end[1]
    res = maze_path_queue(44,63,endx,endy)
    end.reverse()
    if res is None:
        pass
    else:
        env = Maze(end,res[:-1])
        env.draw_res()
        env.mainloop()
        RL = q_learning_model_maze(actions=list(range(env.n_actions)))