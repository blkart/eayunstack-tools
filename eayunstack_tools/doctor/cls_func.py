from eayunstack_tools.utils import get_node_list
from eayunstack_tools.sys_utils import ssh_connect2
import commands
import re
from eayunstack_tools.logger import StackLOG as LOG
from eayunstack_tools.doctor.utils import run_doctor_on_nodes


# get node list for rabbitmq cluster
def get_rabbitmq_nodes():
    running_nodes = []
    (s, o) = commands.getstatusoutput('rabbitmqctl -q cluster_status')
    if s == 0:
        p = re.compile('.*running_nodes,\[([^\]]+)\]', re.S)
        rns = p.findall(o)
        for rn in rns[0].split(','):
            node = rn.strip()
            pp = re.compile(r'\'rabbit@(.+)\'')
            mm = pp.match(node).groups()
            running_nodes.append(mm[0])
    return running_nodes



# get running node list for mysql cluster
def get_mysql_nodes():
    running_nodes = []
    (s, o) = commands.getstatusoutput('crm_resource --locate --resource clone_p_mysql 2> /dev/null | grep "running on"')
    if s != 0 or o is None:
        return
    else:
        for entry in o.split('\n'):
            running_nodes.append(entry.split()[5])
    return running_nodes

# get running node list for haproxy cluster
def get_haproxy_nodes():
    running_nodes = []
    (s, o) = commands.getstatusoutput('crm_resource --locate --resource clone_p_haproxy 2> /dev/null | grep "running on"')
    if s != 0 or o is None:
        return
    else:
        for entry in o.split('\n'):
            running_nodes.append(entry.split()[5])
    return running_nodes


# get ceph cluster status
def ceph_check_health():
    def _log(func, msg):
        func('Ceph cluster check faild !')
        # FIXME: cause the log module issue, need to send error msg line 
        # by line
        for l in msg.split('\n'):
            func(l)

    (s, o) = commands.getstatusoutput('ceph health')
    if s != 0:
        return
    else:
        if o == 'HEALTH_OK':
            LOG.info('Ceph cluster check successfully !')
        else:
            (ss, oo) = commands.getstatusoutput('ceph health detail')
            if o.startswith('HEALTH_WARN'):
                count = len(oo)
                if count > 150:
                    _log(LOG.warn, oo.splitlines()[0])
            else:
                count = len(oo)
                if count > 150:
                    _log(LOG.error, oo.splitlines()[0])


# get ceph osd status
def get_ceph_osd_status():
    (s, o) = commands.getstatusoutput('ceph osd tree')
    if s != 0 or o is None:
        return
    else:
        return o

# get ceph global space
def get_ceph_space():
    (s,o) = commands.getstatusoutput("ceph df | grep 'RAW USED' -A 1 | awk '{print $4}'")
    if s != 0 or o is None:
        return float(-1)
    else:
        space_use = float((o.split("USED\n"))[1])
        return space_use

# check all nodes
def check_all_nodes(check_obj):
    if check_obj is 'all':
        if LOG.enable_debug:
            check_cmd = 'sudo eayunstack --debug doctor cls --all'
        else:
            check_cmd = 'sudo eayunstack doctor cls --all'
    else:
        if LOG.enable_debug:
            check_cmd = 'sudo eayunstack --debug doctor cls -n %s' % check_obj
        else:
            check_cmd = 'sudo eayunstack doctor cls -n %s' % check_obj
    # get controller node list
    node_list = get_node_list('controller')
    # ssh to all controller node to check obj
    if len(node_list) == 0:
        LOG.warn('Node list is null !')
        return
    else:
        if check_obj == 'ceph':
            # only need to check one node for ceph cluster
            ceph_node = node_list[0]
            run_doctor_cmd_on_node('controller', ceph_node, check_cmd)
        else:
            (proc_list, pipe) = run_doctor_on_nodes('controller', node_list, check_cmd)
            for proc in proc_list:
                proc.join()
            LOG.info(pipe.recv(), remote=True)

def get_crm_resource_list():
    resource_list = []
    (s, o) = commands.getstatusoutput('crm_resource -l')
    if s != 0 or o is None:
        return
    else:
        for entry in o.split('\n'):
            if ':' in entry:
                entry = entry.split(':')[0]
                entry = ('clone_' + entry, 'cp')
            else:
                entry = (entry, 'p')
            resource_list.append(entry)
        resource_list = list(set(resource_list))
    return resource_list

def get_crm_resource_running_nodes(resource):
    running_nodes = []
    (s, o) = commands.getstatusoutput('crm_resource --locate --resource %s 2> /dev/null | grep "running on"' % resource)
    if s != 0 or o is None:
        return
    else:
        for entry in o.split('\n'):
            running_nodes.append(entry.split()[5])
    return running_nodes

