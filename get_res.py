import os
import matplotlib.pyplot as plt

SJF_slowdown = 4.0
Random_slowdown = 8.0

target_path = 'test'
file_names = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f))]
file_names.sort(key=lambda l: os.path.getmtime(os.path.join(target_path, l)))

max_rewards, mean_rewards, mean_slowdown = [], [], []

for file_name in file_names:
    with open(os.path.join(target_path, file_name)) as f:
        lines = [line.rstrip().split(' ') for line in f.readlines()]
        max_rewards.append(lines[4][2])
        mean_rewards.append(lines[5][2])
        mean_slowdown.append(lines[6][2])
    f.close()

plt.plot(list(range(0, len(mean_slowdown))), mean_slowdown, label='DeepRM', c='blue')
plt.plot(list(range(0, len(mean_slowdown))), [SJF_slowdown]*len(mean_slowdown), label='SJF', c='green', linestyle='dashed')
plt.plot(list(range(0, len(mean_slowdown))), [Random_slowdown]*len(mean_slowdown), label='Random', c='black', linestyle='dashed')
plt.legend(loc='best')
plt.xlabel('Iteration')
plt.ylabel('Average slowdown')
plt.xlim(0, len(mean_slowdown))
plt.show()
plt.savefig('slowdown.png', format='png')

plt.close()
plt.plot(list(range(0, len(mean_rewards))), mean_rewards, label='DeepRM Mean', c='blue')
plt.plot(list(range(0, len(max_rewards))), max_rewards, label='DeepRM Max', c='red')
plt.legend(loc='best')
plt.xlim(0, len(mean_slowdown))
plt.xlabel('Iteration')
plt.ylabel('Total reward')
plt.savefig('reward.png', format='png')
# plt.show()
