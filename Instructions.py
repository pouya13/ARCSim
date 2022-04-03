""""
Random Instruction Generator (ARCSim)

Written by Pouya Narimani (pouyanarimani.kh@gmail.com).

(c) Copyright SCL, All Rights Reserved. NO WARRANTY.

"""

import numpy as np
import datetime


class Instructions():
    def __init__(self, NI, address):
    	# super(Instructions, self).__init__(parent)
        self.NI = NI
        self.address = address

        self.fetch_instructions_set = []
        self.instructions_set = []


        self.subroutine_counter = 0
        self.min_n_instructions_in_subroutine = 5
        self.max_n_instructions_in_subroutine = 50
        self.n_instructions_in_subroutine = 0
        self.subroutine_len = {}
        self.cnt = 0
        self.subroutine_name_number = 0
        self.instruction_lines = ['\tsleep\n']
        self.stack = [0]
        # self.instruction_lines = ['ss:\n', '\tjmp ss\n']
        self.raw_flag = False

        # print(datetime.datetime.now())
        # print(len(self.instructions_set))


    def set_instructions(self, instructions_set):
        self.instructions_set = instructions_set[0]
        self.fetch_instructions_set = instructions_set[1]


    def subroutine_name(self):
        name = 'sub' + str(self.subroutine_name_number)
        self.subroutine_name_number += 1
        return name

    def instruction_generator(self, fetch=False):
        if self.raw_flag:
            if (self.cnt + 8) < self.NI:
                instruction_number = np.random.randint(0, len(self.instructions_set))
                self.pouya = instruction_number
                self.n_instructions_in_subroutine = np.random.randint(self.min_n_instructions_in_subroutine,
                                                                      self.max_n_instructions_in_subroutine)
            else:
                instruction_number = np.random.randint(0, len(self.fetch_instructions_set))
                self.pouya = instruction_number
                self.n_instructions_in_subroutine = np.random.randint(self.min_n_instructions_in_subroutine,
                                                                      self.max_n_instructions_in_subroutine)

        else:
            if (self.cnt + 1) < self.NI:
                if fetch:
                    instruction_number = np.random.randint(0, len(self.fetch_instructions_set))
                    self.pouya = instruction_number
                    self.n_instructions_in_subroutine = np.random.randint(self.min_n_instructions_in_subroutine,
                                                                          self.max_n_instructions_in_subroutine)
                else:
                    instruction_number = np.random.randint(0, len(self.instructions_set))
                    self.pouya = instruction_number
                    self.n_instructions_in_subroutine = np.random.randint(self.min_n_instructions_in_subroutine,
                                                                          self.max_n_instructions_in_subroutine)
            else:
                instruction_number = np.random.randint(0, len(self.fetch_instructions_set))
                self.pouya = instruction_number
                self.n_instructions_in_subroutine = np.random.randint(self.min_n_instructions_in_subroutine,
                                                                      self.max_n_instructions_in_subroutine)

        ###########################
        ### branch instructions ###
        ###########################

        # rjmp
        if self.instructions_set[instruction_number] == 'rjmp':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                k = 2 * np.random.randint(min_n, max_n)

                # k = 2 * np.random.randint(1, 8)

                k = 2 * 7

                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                k = 2 * np.random.randint(min_n, max_n)

                # k = 2 * np.random.randint(1, 8)
                k = 2 * 7

                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ijmp
        elif self.instructions_set[instruction_number] == 'ijmp':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        #######################################################################################
        # rcall
        elif self.instructions_set[instruction_number] == 'rcall':
            name = self.subroutine_name()
            self.subroutine_len[name] = self.n_instructions_in_subroutine
            instruction = '\t' + self.instructions_set[instruction_number] + ' ' + name + '\n'
            self.instruction_lines.insert(self.stack[-1], instruction)

            self.instruction_lines.append('\n')
            self.instruction_lines.append(name + ':' + '\n')
            self.instruction_lines.append('\tret')
            self.subroutine_len[name] = self.subroutine_len[name] - 1
            self.stack[-1] = self.stack[-1] + 1

            if len(self.subroutine_len) > 1:
                name = list(self.subroutine_len.keys())[-2]
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            self.stack.append(len(self.instruction_lines) - 1)

        # icall
        elif self.instructions_set[instruction_number] == 'icall':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # #######################################################################################
        # # ret
        # elif self.instructions_set[instruction_number] == 'ret':
        # 	print('ok')

        # # reti
        # elif self.instructions_set[instruction_number] == 'reti':
        # 	print('ok')

        # #######################################################################################
        # cpse
        elif self.instructions_set[instruction_number] == 'cpse':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # cp
        elif self.instructions_set[instruction_number] == 'cp':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + 'R' + str(r) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            elif self.cnt < self.NI:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # cpc
        elif self.instructions_set[instruction_number] == 'cpc':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + 'R' + str(r) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            elif self.cnt < self.NI:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # cpi
        elif self.instructions_set[instruction_number] == 'cpi':
            d = np.random.randint(16, 31)
            k = hex(np.random.randint(0, 255))
            if len(k) == 3:
                k = k[:2] + '0' + k[2]
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + k + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            elif self.cnt < self.NI:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + k + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # #######################################################################################
        # sbrc
        elif self.instructions_set[instruction_number] == 'sbrc':
            d = np.random.randint(0, 31)
            k = np.random.randint(0, 7)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + str(k) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            elif self.cnt < self.NI:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sbrs
        elif self.instructions_set[instruction_number] == 'sbrs':
            d = np.random.randint(0, 31)
            k = np.random.randint(0, 7)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + str(k) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            elif self.cnt < self.NI:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sbic
        elif self.instructions_set[instruction_number] == 'sbic':
            a = hex(np.random.randint(0, 31))
            if len(a) == 3:
                a = a[:2] + '0' + a[2]
            k = np.random.randint(0, 7)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + a + ',' + str(k) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            elif self.cnt < self.NI:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + a + ',' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sbis
        elif self.instructions_set[instruction_number] == 'sbis':
            a = hex(np.random.randint(0, 31))
            if len(a) == 3:
                a = a[:2] + '0' + a[2]
            k = np.random.randint(0, 7)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + a + ',' + str(k) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            elif self.cnt < self.NI:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + a + ',' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # #######################################################################################
        # brbs
        elif self.instructions_set[instruction_number] == 'brbs':
            s = np.random.randint(0, 7)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(
                        s) + ',' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(s) + ',' + '.' + str(
                        k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(
                        s) + ',' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(s) + ',' + '.' + str(
                        k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brbc
        elif self.instructions_set[instruction_number] == 'brbc':
            s = np.random.randint(0, 7)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(
                        s) + ',' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(s) + ',' + '.' + str(
                        k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(
                        s) + ',' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(s) + ',' + '.' + str(
                        k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # breq
        elif self.instructions_set[instruction_number] == 'breq':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brne
        elif self.instructions_set[instruction_number] == 'brne':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brcs
        elif self.instructions_set[instruction_number] == 'brcs':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brcc
        elif self.instructions_set[instruction_number] == 'brcc':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brsh
        elif self.instructions_set[instruction_number] == 'brsh':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brlo
        elif self.instructions_set[instruction_number] == 'brlo':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brmi
        elif self.instructions_set[instruction_number] == 'brmi':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brpl
        elif self.instructions_set[instruction_number] == 'brpl':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brge
        elif self.instructions_set[instruction_number] == 'brge':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brlt
        elif self.instructions_set[instruction_number] == 'brlt':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brhs
        elif self.instructions_set[instruction_number] == 'brhs':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brhc
        elif self.instructions_set[instruction_number] == 'brhc':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brts
        elif self.instructions_set[instruction_number] == 'brts':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brtc
        elif self.instructions_set[instruction_number] == 'brtc':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brvs
        elif self.instructions_set[instruction_number] == 'brvs':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brvc
        elif self.instructions_set[instruction_number] == 'brvc':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brie
        elif self.instructions_set[instruction_number] == 'brie':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # brid
        elif self.instructions_set[instruction_number] == 'brid':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                max_n = self.subroutine_len[name]
                min_n = -(self.n_instructions_in_subroutine - self.subroutine_len[name])
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                max_n = self.stack[-1] - self.instruction_lines.index('\tsleep\n') + 1
                min_n = -self.stack[-1]
                max_n = np.minimum(max_n, 63)
                min_n = np.maximum(min_n, -64)
                k = 2 * np.random.randint(min_n, max_n)

                k = 2 * 7
                if k >= 0:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + '+' + str(k) + '\n'
                else:
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + '.' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # #######################################################################################

        ###############################
        ### arithmetic instructions ###
        ###############################

        # adc
        elif self.instructions_set[instruction_number] == 'adc':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # add
        elif self.instructions_set[instruction_number] == 'add':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # adiw
        elif self.instructions_set[instruction_number] == 'adiw':
            d = 2 * np.random.randint(12, 15)
            k = np.random.randint(0, 63)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                # instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                #     d) + '+1' + ':' + 'R' + str(d) + ',' + str(k) + '\n'
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sub
        elif self.instructions_set[instruction_number] == 'sub':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # subi
        elif self.instructions_set[instruction_number] == 'subi':
            d = np.random.randint(16, 31)
            k = hex(np.random.randint(0, 255))
            if len(k) == 3:
                k = k[:2] + '0' + k[2]
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + k + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + k + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sbc
        elif self.instructions_set[instruction_number] == 'sbc':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sbci
        elif self.instructions_set[instruction_number] == 'sbci':
            d = np.random.randint(16, 31)
            k = hex(np.random.randint(0, 255))
            if len(k) == 3:
                k = k[:2] + '0' + k[2]
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + k + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + k + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sbiw
        elif self.instructions_set[instruction_number] == 'sbiw':
            d = 2 * np.random.randint(12, 15)
            k = np.random.randint(0, 63)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                # instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                #     d) + '+1' + ':' + 'R' + str(d) + ',' + str(k) + '\n'
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # #######################################################################################

        ##########################
        ### logic instructions ###
        ##########################

        # and
        elif self.instructions_set[instruction_number] == 'and':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            # d = 0
            # r = 1
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # andi
        elif self.instructions_set[instruction_number] == 'andi':
            d = np.random.randint(16, 31)
            k = hex(np.random.randint(0, 255))
            if len(k) == 3:
                k = k[:2] + '0' + k[2]
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + k + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + k + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # or
        elif self.instructions_set[instruction_number] == 'or':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            # d = 0
            # r = 1
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ori
        elif self.instructions_set[instruction_number] == 'ori':
            d = np.random.randint(16, 31)
            k = hex(np.random.randint(0, 255))
            if len(k) == 3:
                k = k[:2] + '0' + k[2]
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + k + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + k + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1
        # eor
        elif self.instructions_set[instruction_number] == 'eor':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # com
        elif self.instructions_set[instruction_number] == 'com':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # neg
        elif self.instructions_set[instruction_number] == 'neg':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sbr
        elif self.instructions_set[instruction_number] == 'sbr':
            d = np.random.randint(16, 31)
            k = hex(np.random.randint(0, 255))
            if len(k) == 3:
                k = k[:2] + '0' + k[2]
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + k + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + k + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # cbr
        elif self.instructions_set[instruction_number] == 'cbr':
            d = np.random.randint(16, 31)
            k = hex(np.random.randint(0, 255))
            if len(k) == 3:
                k = k[:2] + '0' + k[2]
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + k + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + k + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # inc
        elif self.instructions_set[instruction_number] == 'inc':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # dec
        elif self.instructions_set[instruction_number] == 'dec':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # tst
        elif self.instructions_set[instruction_number] == 'tst':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # clr
        elif self.instructions_set[instruction_number] == 'clr':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ser
        elif self.instructions_set[instruction_number] == 'ser':
            d = np.random.randint(16, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # mul
        elif self.instructions_set[instruction_number] == 'mul':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # muls
        elif self.instructions_set[instruction_number] == 'muls':
            d = np.random.randint(16, 31)
            r = np.random.randint(16, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # mulsu
        elif self.instructions_set[instruction_number] == 'mulsu':
            d = np.random.randint(16, 23)
            r = np.random.randint(16, 23)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # fmul
        elif self.instructions_set[instruction_number] == 'fmul':
            d = np.random.randint(16, 23)
            r = np.random.randint(16, 23)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # fmuls
        elif self.instructions_set[instruction_number] == 'fmuls':
            d = np.random.randint(16, 23)
            r = np.random.randint(16, 23)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # fmulsu
        elif self.instructions_set[instruction_number] == 'fmulsu':
            d = np.random.randint(16, 23)
            r = np.random.randint(16, 23)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # #######################################################################################

        ##################################
        ### data transfer instructions ###
        ##################################

        # mov
        elif self.instructions_set[instruction_number] == 'mov':
            d = np.random.randint(0, 31)
            r = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + 'R' + str(
                    r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # movw
        elif self.instructions_set[instruction_number] == 'movw':
            d = 2 * np.random.randint(0, 15)
            r = 2 * np.random.randint(0, 15)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                # instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                #     d) + '+1:' + 'R' + str(d) + ',' + 'R' + str(r) + '+1:' + 'R' + str(r) + '\n'
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + ',' + 'R' + str(r) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ldi
        elif self.instructions_set[instruction_number] == 'ldi':
            d = np.random.randint(16, 31)
            k = hex(np.random.randint(0, 255))
            if len(k) == 3:
                k = k[:2] + '0' + k[2]
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + k + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + k + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ld X
        elif self.instructions_set[instruction_number] == 'ld_x':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'X' + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'X' + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ld X+
        elif self.instructions_set[instruction_number] == 'ld_x+':
            d = 26
            while (d == 26) or (d == 27):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'X+' + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'X+' + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ld -X
        elif self.instructions_set[instruction_number] == 'ld_-x':
            d = 26
            while (d == 26) or (d == 27):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + '-X' + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + '-X' + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ld Y
        elif self.instructions_set[instruction_number] == 'ld_y':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'Y' + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'Y' + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ld Y+
        elif self.instructions_set[instruction_number] == 'ld_y+':
            d = 28
            while (d == 28) or (d == 29):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'Y+' + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'Y+' + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ld -Y
        elif self.instructions_set[instruction_number] == 'ld_-y':
            d = 28
            while (d == 28) or (d == 29):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + '-Y' + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + '-Y' + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ldd Y
        elif self.instructions_set[instruction_number] == 'ldd_y':
            d = np.random.randint(0, 31)
            q = np.random.randint(0, 63)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'ldd' + ' ' + 'R' + str(d) + ',' + 'Y+' + str(q) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'ldd' + ' ' + 'R' + str(d) + ',' + 'Y+' + str(q) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ld Z
        elif self.instructions_set[instruction_number] == 'ld_z':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'Z' + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'Z' + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ld Z+
        elif self.instructions_set[instruction_number] == 'ld_z+':
            d = 30
            while (d == 30) or (d == 31):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'Z+' + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + 'Z+' + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ld -Z
        elif self.instructions_set[instruction_number] == 'ld_-z':
            d = 30
            while (d == 30) or (d == 31):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + '-Z' + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'ld' + ' ' + 'R' + str(d) + ',' + '-Z' + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ldd Z
        elif self.instructions_set[instruction_number] == 'ldd_z':
            d = np.random.randint(0, 31)
            q = np.random.randint(0, 63)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'ldd' + ' ' + 'R' + str(d) + ',' + 'Z+' + str(q) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'ldd' + ' ' + 'R' + str(d) + ',' + 'Z+' + str(q) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # lds
        elif self.instructions_set[instruction_number] == 'lds':
            d = np.random.randint(0, 31)
            k = hex(np.random.randint(0, 65535))
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                        d) + ',' + k + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(
                    d) + ',' + k + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # st X
        elif self.instructions_set[instruction_number] == 'st_x':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'st' + ' ' + 'X' + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'st' + ' ' + 'X' + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # st X+
        elif self.instructions_set[instruction_number] == 'st_x+':
            d = 26
            while (d == 26) or (d == 27):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'st' + ' ' + 'X+' + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'st' + ' ' + 'X+' + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # st -X
        elif self.instructions_set[instruction_number] == 'st_-x':
            d = 26
            while (d == 26) or (d == 27):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'st' + ' ' + '-X' + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'st' + ' ' + '-X' + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # st Y
        elif self.instructions_set[instruction_number] == 'st_y':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'st' + ' ' + 'Y' + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'st' + ' ' + 'Y' + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # st Y+
        elif self.instructions_set[instruction_number] == 'st_y+':
            d = 28
            while (d == 28) or (d == 29):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'st' + ' ' + 'Y+' + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'st' + ' ' + 'Y+' + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # st -Y
        elif self.instructions_set[instruction_number] == 'st_-y':
            d = 28
            while (d == 28) or (d == 29):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'st' + ' ' + '-Y' + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'st' + ' ' + '-Y' + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # std Y
        elif self.instructions_set[instruction_number] == 'std_y':
            d = np.random.randint(0, 31)
            q = np.random.randint(0, 63)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'std' + ' ' + 'Y+' + str(q) + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'std' + ' ' + 'Y+' + str(q) + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # st Z
        elif self.instructions_set[instruction_number] == 'st_z':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'st' + ' ' + 'Z' + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'st' + ' ' + 'Z' + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # st Z+
        elif self.instructions_set[instruction_number] == 'st_z+':
            d = 30
            while (d == 30) or (d == 31):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'st' + ' ' + 'Z+' + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'st' + ' ' + 'Z+' + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # st -Z
        elif self.instructions_set[instruction_number] == 'st_-z':
            d = 30
            while (d == 30) or (d == 31):
                d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'st' + ' ' + '-Z' + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'st' + ' ' + '-Z' + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # std Z
        elif self.instructions_set[instruction_number] == 'std_z':
            d = np.random.randint(0, 31)
            q = np.random.randint(0, 63)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'std' + ' ' + 'Z+' + str(q) + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'std' + ' ' + 'Z+' + str(q) + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sts
        elif self.instructions_set[instruction_number] == 'sts':
            d = np.random.randint(0, 31)
            k = hex(np.random.randint(0, 65535))
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + k + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + k + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # lpm
        elif self.instructions_set[instruction_number] == 'lpm':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # lpm Z
        elif self.instructions_set[instruction_number] == 'lpm_z':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'lpm' + ' ' + 'R' + str(d) + ',' + 'Z'  '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'lpm' + ' ' + 'R' + str(d) + ',' + 'Z'  '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # lpm Z+
        elif self.instructions_set[instruction_number] == 'lpm_z+':
            d = np.random.randint(0, 29)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + 'lpm' + ' ' + 'R' + str(d) + ',' + 'Z+'  '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + 'lpm' + ' ' + 'R' + str(d) + ',' + 'Z+'  '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # spm
        elif self.instructions_set[instruction_number] == 'spm':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # in
        elif self.instructions_set[instruction_number] == 'in':
            d = np.random.randint(0, 31)
            k = '0x18'
            while (k=='0x17') or (k=='0x18') or (k == '0x0d') or (k == '0x2f') or (k == '0x1c') or (k == '0x1d') or (k == '0x1e') or (k == '0x1f'):
                k = hex(np.random.randint(0, 63))
            if len(k) == 3:
                k = k[:2] + '0' + k[2]
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + ',' + k +  '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + ',' + k +  '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # out
        elif self.instructions_set[instruction_number] == 'out':
            d = np.random.randint(0, 31)
            k = '0x17'
            while (k == '0x17') or (k == '0x18') or (k == '0x0d') or (k == '0x2f') or (k == '0x1c') or (k == '0x1d') or (k == '0x1e') or (k == '0x1f'):
                k = hex(np.random.randint(0, 63))
            if len(k) == 3:
                k = k[:2] + '0' + k[2]
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + k + ',' + 'R' + str(d) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + k + ',' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # push
        elif self.instructions_set[instruction_number] == 'push':
            d = np.random.randint(0, 31)
            # if len(self.subroutine_len) > 0:
            #     name = list(self.subroutine_len.keys())[-1]
            #     instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
            #     self.instruction_lines.insert(self.stack[-1], instruction)
            #     self.subroutine_len[name] = self.subroutine_len[name] - 1
            #     self.stack[-1] = self.stack[-1] + 1
            #
            #     if self.subroutine_len[name] == 0:
            #         self.subroutine_len.pop(name)
            #         self.stack.pop(-1)
            if len(self.subroutine_len) == 0:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # pop
        elif self.instructions_set[instruction_number] == 'pop':
            d = np.random.randint(0, 31)
            # if len(self.subroutine_len) > 0:
            #     name = list(self.subroutine_len.keys())[-1]
            #     instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
            #     self.instruction_lines.insert(self.stack[-1], instruction)
            #     self.subroutine_len[name] = self.subroutine_len[name] - 1
            #     self.stack[-1] = self.stack[-1] + 1
            #
            #     if self.subroutine_len[name] == 0:
            #         self.subroutine_len.pop(name)
            #         self.stack.pop(-1)
            if len(self.subroutine_len) == 0:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # #######################################################################################

        #####################################
        ### bit and bit_test instructions ###
        #####################################

        # sbi
        elif self.instructions_set[instruction_number] == 'sbi':
            a = '0x17'
            while (a=='0x17') or (a=='0x18'):
                a = hex(np.random.randint(0, 31))
            if len(a) == 3:
                a = a[:2] + '0' + a[2]
            k = np.random.randint(0, 7)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + a + ',' + str(k) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + a + ',' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # cbi
        elif self.instructions_set[instruction_number] == 'cbi':
            a = '0x17'
            while (a == '0x17') or (a == '0x18'):
                a = hex(np.random.randint(0, 31))
            if len(a) == 3:
                a = a[:2] + '0' + a[2]
            k = np.random.randint(0, 7)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + a + ',' + str(k) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + a + ',' + str(k) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # lsl
        elif self.instructions_set[instruction_number] == 'lsl':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # lsr
        elif self.instructions_set[instruction_number] == 'lsr':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # rol
        elif self.instructions_set[instruction_number] == 'rol':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ror
        elif self.instructions_set[instruction_number] == 'ror':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # asr
        elif self.instructions_set[instruction_number] == 'asr':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # swap
        elif self.instructions_set[instruction_number] == 'swap':
            d = np.random.randint(0, 31)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(d) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # bset
        elif self.instructions_set[instruction_number] == 'bset':
            # s = np.random.randint(0, 7) for enabling interrups flag (bit 7)
            s = np.random.randint(0, 6)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(s) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(s) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # bclr
        elif self.instructions_set[instruction_number] == 'bclr':
            s = np.random.randint(0, 7)
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(s) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)
            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + str(s) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # bst
        elif self.instructions_set[instruction_number] == 'bst':
            r = np.random.randint(0, 31)
            b = np.random.randint(0, 7)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(r) + ',' + str(b) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(r) + ',' + str(b) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # bld
        elif self.instructions_set[instruction_number] == 'bld':
            r = np.random.randint(0, 31)
            b = np.random.randint(0, 7)
            if len(self.subroutine_len) > 0:
                if self.subroutine_len[list(self.subroutine_len.keys())[-1]] > 1:
                    name = list(self.subroutine_len.keys())[-1]
                    instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(r) + ',' + str(b) + '\n'
                    self.instruction_lines.insert(self.stack[-1], instruction)
                    self.subroutine_len[name] = self.subroutine_len[name] - 1
                    self.stack[-1] = self.stack[-1] + 1

                    if self.subroutine_len[name] == 0:
                        self.subroutine_len.pop(name)
                        self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + ' ' + 'R' + str(r) + ',' + str(b) + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sec
        elif self.instructions_set[instruction_number] == 'sec':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # clc
        elif self.instructions_set[instruction_number] == 'clc':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sen
        elif self.instructions_set[instruction_number] == 'sen':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # cln
        elif self.instructions_set[instruction_number] == 'cln':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sez
        elif self.instructions_set[instruction_number] == 'sez':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # clz
        elif self.instructions_set[instruction_number] == 'clz':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sei
        elif self.instructions_set[instruction_number] == 'sei':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # cli
        elif self.instructions_set[instruction_number] == 'cli':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # ses
        elif self.instructions_set[instruction_number] == 'ses':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # cls
        elif self.instructions_set[instruction_number] == 'cls':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # sev
        elif self.instructions_set[instruction_number] == 'sev':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # clv
        elif self.instructions_set[instruction_number] == 'clv':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # set
        elif self.instructions_set[instruction_number] == 'set':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # clt
        elif self.instructions_set[instruction_number] == 'clt':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # seh
        elif self.instructions_set[instruction_number] == 'seh':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # clh
        elif self.instructions_set[instruction_number] == 'clh':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # nop
        elif self.instructions_set[instruction_number] == 'nop':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1

        # wdr
        elif self.instructions_set[instruction_number] == 'wdr':
            if len(self.subroutine_len) > 0:
                name = list(self.subroutine_len.keys())[-1]
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.subroutine_len[name] = self.subroutine_len[name] - 1
                self.stack[-1] = self.stack[-1] + 1

                if self.subroutine_len[name] == 0:
                    self.subroutine_len.pop(name)
                    self.stack.pop(-1)

            else:
                instruction = '\t' + self.instructions_set[instruction_number] + '\n'
                self.instruction_lines.insert(self.stack[-1], instruction)
                self.stack[-1] = self.stack[-1] + 1


    def generate_new_framed_code(self, filename):
        while self.cnt < self.NI:
            # if (self.cnt % 3 == 0):
            # self.instruction_lines.insert(self.stack[-1], '\tout 0x18, R17\n')
            # self.instruction_lines.insert(self.stack[-1], '\tsbi 0x05, 2\n')
            self.instruction_lines.insert(self.stack[-1], '\tsbi 0x18, 2\n')
            self.stack[-1] = self.stack[-1] + 1
            self.instruction_lines.insert(self.stack[-1], '\tnop\n')
            self.stack[-1] = self.stack[-1] + 1


            xxx = len(self.instruction_lines)
            self.instruction_generator(fetch=False)

            if (len(self.instruction_lines)-xxx)==0:
                print(self.instructions_set[self.pouya])
                print('####################################')
            
            xxx = len(self.instruction_lines)
            self.instruction_generator()
            
            if (len(self.instruction_lines)-xxx)==0:
                print(self.instructions_set[self.pouya])
                print('####################################')
            
            xxx = len(self.instruction_lines)
            self.instruction_generator(fetch=False)
            
            if (len(self.instruction_lines)-xxx)==0:
                print(self.instructions_set[self.pouya])
                print('####################################')


            self.instruction_lines.insert(self.stack[-1], '\tnop\n')
            self.stack[-1] = self.stack[-1] + 1

            self.instruction_lines.insert(self.stack[-1], '\tcbi 0x18, 2\n')
            self.stack[-1] = self.stack[-1] + 1

            self.cnt += 1

        self.instruction_lines.insert(0, '\n')
        self.instruction_lines.insert(0, '\tsbi 0x17, 2\n')

        self.instruction_lines.insert(0, '\n')
        self.instruction_lines.insert(0, '\tclh\n')
        self.instruction_lines.insert(0, '\tclt\n')
        self.instruction_lines.insert(0, '\tclv\n')
        self.instruction_lines.insert(0, '\tcls\n')
        self.instruction_lines.insert(0, '\tclz\n')
        self.instruction_lines.insert(0, '\tcln\n')
        self.instruction_lines.insert(0, '\tclc\n')
        self.instruction_lines.insert(0, '\tmov R0, R16\n')
        self.instruction_lines.insert(0, '\tmov R1, R16\n')
        self.instruction_lines.insert(0, '\tmov R2, R16\n')
        self.instruction_lines.insert(0, '\tmov R3, R16\n')
        self.instruction_lines.insert(0, '\tmov R4, R16\n')
        self.instruction_lines.insert(0, '\tmov R5, R16\n')
        self.instruction_lines.insert(0, '\tmov R6, R16\n')
        self.instruction_lines.insert(0, '\tmov R7, R16\n')
        self.instruction_lines.insert(0, '\tmov R8, R16\n')
        self.instruction_lines.insert(0, '\tmov R9, R16\n')
        self.instruction_lines.insert(0, '\tmov R10, R16\n')
        self.instruction_lines.insert(0, '\tmov R11, R16\n')
        self.instruction_lines.insert(0, '\tmov R12, R16\n')
        self.instruction_lines.insert(0, '\tmov R13, R16\n')
        self.instruction_lines.insert(0, '\tmov R14, R16\n')
        self.instruction_lines.insert(0, '\tmov R15, R16\n')
        self.instruction_lines.insert(0, '\tldi R16, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R17, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R18, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R19, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R20, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R21, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R22, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R23, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R24, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R25, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R26, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R27, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R28, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R29, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R30, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R31, 0x00\n')

        f = open(self.address + filename, 'w')
        f.writelines(self.instruction_lines)
        f.close()


    def generate_new_raw_code(self, filename):
        self.raw_flag = True
        while self.cnt < self.NI:
            # xxx = len(self.instruction_lines)
            # self.instruction_generator(fetch=True)

            # if (len(self.instruction_lines)-xxx)==0:
            #     print(self.instructions_set[self.pouya])
            #     print('####################################')

            my_flag = True
            xxx = len(self.instruction_lines)
            while my_flag:
                my_flag = False
                self.instruction_generator()
                
                if (len(self.instruction_lines)-xxx)==0:
                    my_flag = True
            
            # xxx = len(self.instruction_lines)
            # self.instruction_generator(fetch=True)

            # print(self.branch_flag)
            # print('############################')
            
            # if (len(self.instruction_lines)-xxx)==0:
            #     print(self.instructions_set[self.pouya])
            #     print('####################################')

            self.cnt += 1

        self.instruction_lines.insert(self.stack[-1], '\tcbi 0x18, 2\n')
        self.stack[-1] = self.stack[-1] + 1
        self.instruction_lines.insert(self.stack[-1], '\n')
        self.stack[-1] = self.stack[-1] + 1

        self.instruction_lines.insert(0, '\n')
        self.instruction_lines.insert(0, '\tsbi 0x17, 2\n')

        self.instruction_lines.insert(0, '\n')
        self.instruction_lines.insert(0, '\tclh\n')
        self.instruction_lines.insert(0, '\tclt\n')
        self.instruction_lines.insert(0, '\tclv\n')
        self.instruction_lines.insert(0, '\tcls\n')
        self.instruction_lines.insert(0, '\tclz\n')
        self.instruction_lines.insert(0, '\tcln\n')
        self.instruction_lines.insert(0, '\tclc\n')
        self.instruction_lines.insert(0, '\tmov R0, R16\n')
        self.instruction_lines.insert(0, '\tmov R1, R16\n')
        self.instruction_lines.insert(0, '\tmov R2, R16\n')
        self.instruction_lines.insert(0, '\tmov R3, R16\n')
        self.instruction_lines.insert(0, '\tmov R4, R16\n')
        self.instruction_lines.insert(0, '\tmov R5, R16\n')
        self.instruction_lines.insert(0, '\tmov R6, R16\n')
        self.instruction_lines.insert(0, '\tmov R7, R16\n')
        self.instruction_lines.insert(0, '\tmov R8, R16\n')
        self.instruction_lines.insert(0, '\tmov R9, R16\n')
        self.instruction_lines.insert(0, '\tmov R10, R16\n')
        self.instruction_lines.insert(0, '\tmov R11, R16\n')
        self.instruction_lines.insert(0, '\tmov R12, R16\n')
        self.instruction_lines.insert(0, '\tmov R13, R16\n')
        self.instruction_lines.insert(0, '\tmov R14, R16\n')
        self.instruction_lines.insert(0, '\tmov R15, R16\n')
        self.instruction_lines.insert(0, '\tldi R16, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R17, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R18, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R19, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R20, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R21, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R22, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R23, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R24, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R25, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R26, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R27, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R28, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R29, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R30, 0x00\n')
        self.instruction_lines.insert(0, '\tldi R31, 0x00\n')


        f = open(self.address + filename, 'w')
        f.writelines(self.instruction_lines)
        f.close()
        