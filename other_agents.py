import numpy as np


def get_packer_action(machines, job_slot):
        align_score = 0
        act = len(job_slot.slot)  # if no action available, hold

        for i in xrange(len(job_slot.slot)):
            new_job = job_slot.slot[i]
            if new_job is not None:  # there is a pending job
                
                can_allocate, idx_of_abvl_res = machines.can_allocate_to_multimachines(new_job)
                if can_allocate: # enough resource to allocate
                    idx_of_res_alloc = [[] for i in range(machines.num_machines)] ##list of resource indices to be allocated per machine

                    for res_idx, machine_idxs in enumerate(idx_of_abvl_res):
                        idx_of_res_alloc[machine_idxs[0]].append(res_idx) #take the first index for now

                    tmp_align_score = 0
                    for machine_idx, res_alloc_list in enumerate(idx_of_res_alloc):
                        for res_idx in res_alloc_list:
                            avbl_res = machines.machinelist[machine_idx].avbl_slot[:new_job.len, :]
                            tmp_align_score += avbl_res[0, res_idx] * (new_job.res_vec[res_idx]) 

                    if tmp_align_score > align_score:
                        align_score = tmp_align_score
                        act = i
        return act


def get_sjf_action(machines, job_slot):
        sjf_score = 0
        act = len(job_slot.slot)  # if no action available, hold

        for i in xrange(len(job_slot.slot)):
            new_job = job_slot.slot[i]
            if new_job is not None:  # there is a pending job

                can_allocate, _ = machines.can_allocate_to_multimachines(new_job)

                if can_allocate: # enough resource to allocate
                    
                    tmp_sjf_score = 1 / float(new_job.len)

                    if tmp_sjf_score > sjf_score:
                        sjf_score = tmp_sjf_score
                        act = i
        return act


def get_packer_sjf_action(machines, job_slot, knob):  # knob controls which to favor, 1 to packer, 0 to sjf

        combined_score = 0
        act = len(job_slot.slot)  # if no action available, hold

        for i in xrange(len(job_slot.slot)):
            new_job = job_slot.slot[i]
            if new_job is not None:  # there is a pending job

                can_allocate, idx_of_abvl_res = machines.can_allocate_to_multimachines(new_job)
                
                if can_allocate: # enough resource to allocate
                    idx_of_res_alloc = [[] for i in range(machines.num_machines)] ##list of resource indices to be allocated per machine

                    for res_idx, machine_idxs in enumerate(idx_of_abvl_res):
                        idx_of_res_alloc[machine_idxs[0]].append(res_idx) #take the first index for now

                    tmp_align_score = 0
                    for machine_idx, res_alloc_list in enumerate(idx_of_res_alloc):
                        for res_idx in res_alloc_list:
                            avbl_res = machines.machinelist[machine_idx].avbl_slot[:new_job.len, :]
                            tmp_align_score += avbl_res[0, res_idx] * (new_job.res_vec[res_idx]) 

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
