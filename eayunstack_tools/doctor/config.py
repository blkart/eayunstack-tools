
# OpenStack component's profiles and service name manifest
# 'XXX_p' for XXX's profiles list

keystone_p = [
        '/etc/keystone/keystone.conf'
        ]

glance_p = [
        '/etc/glance/glance-api.conf',
        '/etc/glance/glance-registry.conf',
        ]

neutron_p = [
        '/etc/neutron/neutron.conf'
        ]

nova_p = [
        '/etc/nova/nova.conf'
        ]

cinder_p = [
        '/etc/cinder/cinder.conf'
    ]

ceilometer_p = [
        '/etc/ceilometer/ceilometer.conf'
        ]

mongo_p = [
        '/etc/mongodb.conf'
        ]

controller_ceph_p = [
        '/etc/ceph/ceph.conf'
        ]

ceph_osd_ceph_p = [
        '/etc/ceph/ceph.conf'
        ]

# 'XXX_s' for XXX's services list

keystone_s = [
        'openstack-keystone'
        ]

glance_s = [
        'openstack-glance-api',
        'openstack-glance-registry'
        ]

neutron_s = [
        'neutron-server',
        'neutron-ovs-cleanup',
        'openvswitch',
        'neutron-metering-agent'
    ]

controller_nova_s = [
        'openstack-nova-api',
        'openstack-nova-conductor',
        'openstack-nova-scheduler'
        ]

compute_nova_s = [
        'openstack-nova-compute',
        'openstack-ceilometer-compute'
        ]

cinder_s = [
        'openstack-cinder-api',
        'openstack-cinder-scheduler',
        'openstack-cinder-volume'
    ]

ceilometer_s = [
        'openstack-ceilometer-alarm-notifier',
        'openstack-ceilometer-collector',
        'openstack-ceilometer-notification',
        'httpd'
        ]

mongo_s = [
        'mongod'
        ]

controller_ceph_s = [
        ]

ceph_osd_ceph_s = [
        ]

# component db profile list

component_db_p = {
        'keystone':'/etc/keystone/keystone.conf',
        'glance':'/etc/glance/glance-registry.conf',
        'nova':'/etc/nova/nova.conf',
        'neutron':'/etc/neutron/neutron.conf',
        'cinder':'/etc/cinder/cinder.conf',
        'ceilometer':'/etc/ceilometer/ceilometer.conf'
        }

# component availability check command

component_check_cmd = {
        'keystone':'keystone tenant-list',
        'glance':'glance image-list',
        'nova':'nova list',
        'neutron':'PYTHONIOENCODING=utf-8 neutron net-list',
        'cinder':'cinder list',
        'ceilometer':'ceilometer sample-list -m image -l 1'
        }

# component list for every node

controller_c = [
        'keystone',
        'glance',
        'nova',
        'neutron',
        'cinder',
        'ceilometer',
        'ceph'
        ]

compute_c = [
        'nova'
        ]

mongo_c = [
        'mongo'
        ]

ceph_osd_c = [
        'ceph'
        ]

# return profile list

def get_keystone_profiles():
    return keystone_p

def get_glance_profiles():
    return glance_p

def get_nova_profiles():
    return nova_p

def get_neutron_profiles():
    return neutron_p

def get_cinder_profiles():
    return cinder_p

def get_ceilometer_profiles():
    return ceilometer_p

def get_mongo_profiles():
    return mongo_p

def get_controller_ceph_profiles():
    return controller_ceph_p

def get_ceph_osd_ceph_profiles():
    return ceph_osd_ceph_p

# return services list

def get_keystone_services():
    return keystone_s

def get_glance_services():
    return glance_s

def get_controller_nova_services():
    return controller_nova_s

def get_compute_nova_services():
    return compute_nova_s

def get_neutron_services():
    return neutron_s

def get_cinder_services():
    return cinder_s

def get_ceilometer_services():
    return ceilometer_s

def get_mongo_services():
    return mongo_s

def get_controller_ceph_services():
    return controller_ceph_s

def get_ceph_osd_ceph_services():
    return ceph_osd_ceph_s

# return db profile

def get_db_profile():
    return component_db_p

# return components list

def get_controller_component():
    return controller_c

def get_compute_component():
    return compute_c

def get_mongo_component():
    return mongo_c

def get_ceph_osd_component():
    return ceph_osd_c

# return a list of commands for check component availability

def get_component_check_cmd():
    return component_check_cmd
