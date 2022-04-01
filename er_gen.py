#!/usr/bin/python3.7
# -*- coding: utf-8
version = 'Edge_Config_Creator Version 1.0'

import re
import os
import shutil
work_dir = os.path.dirname(os.path.abspath(__file__))


def edit_conf(dev_type, name, net, ssh, http, https, dns1, dns2, out_ip, out_gw, time_zone):

    # Создаем временную папку из шаблона
    shutil.copytree(f"{work_dir}/def_config", f"{work_dir}/{name}/config")
    # Копируем конфиг-файл
    shutil.copyfile(f"{work_dir}/config_boot_files/config.boot_{dev_type}", 
                    f"{work_dir}/{name}/config/config.boot")
    # Правим конфиг
    with open(f"{work_dir}/{name}/config/config.boot", 'r+') as f:
        f_list = list(f.readlines())

    for n, row in enumerate(f_list):
        if re.search(r'%IP%', row):
            nline = re.sub(r'%IP%', net, row)
        elif re.search(r'%NAME%', row):
            nline = re.sub(r'%NAME%', name, row)
        elif re.search(r'%SSH%', row):
            nline = re.sub(r'%SSH%', ssh, row)
        elif re.search(r'%HTTP%', row):
            nline = re.sub(r'%HTTP%', http, row)
        elif re.search(r'%HTTPS%', row):
            nline = re.sub(r'%HTTPS%', https, row)
        elif re.search(r'%DNS1%', row):
            nline = re.sub(r'%DNS1%', dns1, row)
        elif re.search(r'%DNS2%', row):
            nline = re.sub(r'%DNS2%', dns2, row)
        elif re.search(r'%OUTIP%', row):
            nline = re.sub(r'%OUTIP%', out_ip, row)
        elif re.search(r'%OUTGW%', row):
            nline = re.sub(r'%OUTGW%', out_gw, row)
        elif re.search(r'%TZONE%', row):
            nline = re.sub(r'%TZONE%', time_zone, row)
        else:
            nline = row
        f_list[n] = nline

    with open(f"{work_dir}/{name}/config/config.boot", 'w+') as f:
        for line in f_list:
            f.write(line)

    # Заливаем конфиги в архив
    print('Собираю архив...')
    shutil.make_archive(f"{work_dir}/{name}", 'gztar', f"{work_dir}/{name}")

    # Удаляем временные папки
    shutil.rmtree(f"{work_dir}/{name}")
    print('Готово!')


def run():
    
    dev_type = input('Выберите тип устройства (er4, er6p, lite) = ')
    if dev_type == 'er4' or dev_type == 'er6p' or dev_type == 'lite':

        if input('Сменить имя и адрессацию локальной сети? y/n = ') == 'y':
            name = input('NAME = ')
            input_net = input('IP (первые 3 актета) = ')
            if re.search(r'^[0-9]{1,3}[\.][0-9]{1,3}[\.][0-9]{1,3}$', input_net):
                net = input_net
            else:
                net = '192.168.100'
        else:
            name, net = 'Router', '192.168.100'

        if input('Сменить стандартные порты? y/n = ') == 'y':
            ssh = input('SSH = ')
            http = input('HTTP = ')
            https = input('HTTPS = ')
        else:
            ssh, http, https = '22', '80', '443'

        if input('Сменить стандартные DNS (от Google по умолчанию)? y/n = ') == 'y':
            dns1 = input('DNS1 = ')
            dns2 = input('DNS2 = ')
        else:
            dns1, dns2 = '8.8.8.8', '8.8.4.4'

        if input('Ввести настройки провайдера? y/n = ') == 'y':
            out_ip = input('OUT_IP = ')
            out_gw = input('OUT_GW = ')
        else:
            out_ip, out_gw = '192.168.1.1', '192.168.1.251'

        if input('Сменить часовой пояс? (Asia/Yekaterinburg по умолчанию) y/n = ') == 'y':
            time_zone = input('TimeZone = ')
        else:
            time_zone = 'Asia/Yekaterinburg'

        edit_conf(dev_type, name, net, ssh, http, https, dns1, dns2, out_ip, out_gw, time_zone)

    else:
        print('Введен не корректный тип устройства!')
    

run()

