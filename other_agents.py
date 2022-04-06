# Other scheduling algorithms: packer, SJF, and a combo of them 
import numpy as np

def get_packer_action(machine, job_slot):
        align_score = 0
        act = len(job_slot.slot)  # if no action available, hold

        for i in xrange(len(job_slot.slot)):
            new_job = job_slot.slot[i]
            if new_job is not None:  # there is a pending job

                avbl_res = machine.avbl_slot[:new_job.len, :]
                res_left = avbl_res - new_job.res_vec

                if np.all(res_left[:] >= 0):  # enough resource to allocate

                    # get score from dot product of available resources and resources requested by the new job
                    tmp_align_score = avbl_res[0, :].dot(new_job.res_vec)

                    # get the highest ranking job
                    if tmp_align_score > align_score:
                        align_score = tmp_align_score
                        act = i

        return act

# find the shortest job in job_slot
def get_sjf_action(machine, job_slot):
        sjf_score = 0
        act = len(job_slot.slot)  # if no action available, hold

        for i in xrange(len(job_slot.slot)):
            new_job = job_slot.slot[i]
            if new_job is not None:  # there is a pending job

                avbl_res = machine.avbl_slot[:new_job.len, :]
                res_left = avbl_res - new_job.res_vec

                if np.all(res_left[:] >= 0):  # enough resource to allocate

                    tmp_sjf_score = 1 / float(new_job.len)

                    if tmp_sjf_score > sjf_score:
                        sjf_score = tmp_sjf_score
                        act = i
        return act

def get_packer_sjf_action(machine, job_slot, knob):  # knob controls which to favor, 1 to packer, 0 to sjf

        combined_score = 0
        act = len(job_slot.slot)  # if no action available, hold

        for i in xrange(len(job_slot.slot)):
            new_job = job_slot.slot[i]
            if new_job is not None:  # there is a pending job

                avbl_res = machine.avbl_slot[:new_job.len, :]
                res_left = avbl_res - new_job.res_vec

                if np.all(res_left[:] >= 0):  # enough resource to allocate

                    tmp_align_score = avbl_res[0, :].dot(new_job.res_vec)
                    tmp_sjf_score = 1 / float(new_job.len)

                    tmp_combined_score = knob * tmp_align_score + (1 - knob) * tmp_sjf_score

                    if tmp_combined_score > combined_score:
                        combined_score = tmp_combined_score
                        act = i
        return act


def get_random_action(job_slot):
    num_act = len(job_slot.slot) + 1  # if no action available,
    act = np.random.randint(num_act)
    return act

    def machine_available(machine, new_job):
        avbl_res = machine.avbl_slot[:new_job.len, :]
        res_left = avbl_res - new_job.res_vec
        return np.all(res_left[:] >= 0)

    def get_action(machines, job_slot, midx, end_idx, knob):
        sjf_score_list = [1.0 / job_slot.slot[i].len if job_slot.slot[i] is not None else -1 for i in
                          xrange(len(job_slot.slot))]
        packer_score_list = []
        for i in xrange(len(job_slot.slot)):
            new_job = job_slot.slot[i]
            new_job_score = -1
            if new_job is not None:  # there is a pending job
                avbl_res = machines[midx].avbl_slot[:new_job.len, :]
                res_left = avbl_res - new_job.res_vec
                if np.all(res_left[:] >= 0):  # enough resource to allocate
                    new_job_score = avbl_res[0, :].dot(new_job.res_vec)

            packer_score_list.append(new_job_score)

        total_score_list = [i + knob * j for i in sjf_score_list for j in packer_score_list]

        if np.all(np.asarray(total_score_list[:]) < 0):
            if end_idx == midx:
                return len(job_slot.slot) * len(machines)
            else:
                return get_action(machines, job_slot, (midx+1) % len(machines), end_idx, knob)
        else:
            a = np.argmax(total_score_list)
            return a

    midx = 0
    for idx in xrange(len(machines)):
        if machines[idx].turn_to_allocate:
            midx = idx
            break

    end_idx = midx - 1 if midx > 0 else len(machines) - 1
    return get_action(machines, job_slot, midx, end_idx, knob)



