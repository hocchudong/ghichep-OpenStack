# 1. Mô hình mạng

![](https://github.com/hocchudong/ghichep-OpenStack/blob/master/13-Kolla/kolla-ansible/images/openstack-mitaka-network-layout.png?raw=true)

- Cài đặt phiên bản openstack mitaka trên 2 node controller và compute.

### Các yêu cầu về phiên bản phần mềm đối với openstack mitaka.
| Component | Min Version | Max Version | Comment |
|:-------|:------:|-------:|-------:|
| Ansible | 1.9.4 | <2.0.0 | On deployment host |
| Docker | 1.10.0 | none | On target nodes |
| Docker Python | 1.6.0 | none | On target nodes |
| Python Jinja2 | 2.6.0 | none | On deployment host |

#### Note: Thực hiện lần lượt các bước. Ở từng bước có chú thích là:
  - **all**: Tương ứng là thực hiện trên cả 2 node.
  - **controller**: Thực hiện trên node controller.
  - **compute**: Thực hiện trên node compute.

## 1. Upgrade the kernel (all)
```sh
apt-get update && apt-get -y install linux-image-generic-lts-wily
```

## 2. Modify the hosts
- On controller
```sh
vi /etc/hostname
controller
```

- On compute
```sh
vi /etc/hostname
compute
```

- On all
```sh
127.0 .0 .1 localhost
10.10.10.10     controller
10.10.10.20     compute
```

## 3. Install Docker (all)
```sh
curl -sSL https://get.docker.io | bash
usermod -aG docker root
mount --make-shared /run
service docker restart
apt-get install -y python-pip
pip install -U docker-py
```

## 4. Install NTP (all)
```sh
apt-get install ntp -y
```

## 5. Install Ansible (controller)
```sh
apt-get install -y software-properties-common
pip install ansible==1.9.6
```

## 6. Install the ssh key (all)
- Cho phép login với user root
```sh
$ vi /etc/ssh/sshd_config
"PermitRootLogin Without-password" -> "PermitRootLogin yes"
$ sudo service ssh restart
```

- Tạo và trao đổi khóa cho 2 node.
```sh
[root@controller ~]# ssh-keygen
[root@compute ~]# ssh-keygen
[root@controller .ssh]# scp root@compute:~/.ssh/id_rsa.pub id_rsa_compute.pub
[root@controller .ssh]# cat id_rsa.pub >> ~/.ssh/authorized_keys
[root@controller .ssh]# cat id_rsa_compute.pub >> ~/.ssh/authorized_keys
[root@controller .ssh]# scp authorized_keys root@compute:~/.ssh/authorized_keys
```

## 7. Install the openstack client Install the Openstack client (controller)
```sh
apt-get install -y python-dev libffi-dev libssl-dev gcc
pip install -U python-openstackclient python-neutronclient
```

## 8. Installing the Kolla (controller)
- Clone Kolla projects: Mitaka.
```sh
git clone -b stable/mitaka https://github.com/openstack/kolla.git
```

- Install Kolla tools and dependencies:
```sh
pip install kolla/ (đang ở thư mục cha của thư mục kolla)
```

- Nếu lỗi, chạy các lệnh sau, và tiến hành chạy lại lệnh trên
```sh
apt-get purge -y python-pip
wget https://bootstrap.pypa.io/get-pip.py
python ./get-pip.py
apt-get install python-pip
```

- Copy file config kolla:
```sh
$ sudo cd kolla
$ sudo cp -r etc/kolla /etc/
```

## 9. Configure the local Docker repository

### 9.1. Start the Registry (controller)
```sh
docker run -d -p 4000:5000 --restart=always --name registry registry:2
```

### 9.2. Modify the docker daemon default parameters (all)
```sh
vi /etc/default/docker
DOCKER_OPTS="--insecure-registry 10.10.10.10:4000"
service docker restart
```

## 10. Modify the configuration of Kolla (controller)
```sh
vi /usr/local/share/kolla/ansible/inventory/multinode
```

Cấu hình các thành phần sẽ được cài đặt trên các node. Ở đây, tôi cấu hình phần compute sẽ chạy trên node compute, các thành phần còn lại chạy trên node controller.
```sh
[control]
# These hostname must be resolvable from your deployment host
 controller
# The network nodes are where your l3-agent and loadbalancers will run
# This can be the same as a host in the control group
[network]
controller
[compute]
compute
[storage]
controller
...
```

## 11. Compile openstack the docker image (controller)
```sh
kolla-build --base ubuntu --type source --registry 10.10.10.10:4000 --push
```

## 12. Deploy Kolla (controller)
```sh
vi /etc/kolla/globals.yml
```

- Cấu hình các thông tin tương ứng.
```sh
Kolla_base_distro:  "ubuntu"
kolla_install_type:  "source"
kolla_internal_vip_address:  "10.10.10.50"
network_interface:  "eth0"
neutron_external_interface:  "eth1"
docker_registry:  "10.10.10.10:4000"
...
```

- Sau khi cấu hình, chạy các lệnh sau:
```sh
kolla-genpwd  #Gen password các services.
kolla-ansible prechecks -i /usr/local/share/kolla/ansible/inventory/multinode   #Check before deploy.
kolla-ansible deploy -i /usr/local/share/kolla/ansible/inventory/multinode      #Deploy.
```

## 13. Generate an openrc file (controller)
```sh
kolla-ansible post-deploy
```

- Đến đây, quá trình cài đặt đã hoàn tất.
- Ngoài ra, Openstack còn cung cấp cho ta các scripts tự động hóa thực hiện các công việc như:
  - Upload cirros image và tạo một mảng ảo.
  ```sh
  source /etc/kolla/admin-openrc.sh
  kolla/tools/init-runonce
  ```
  - Xóa các containers openstack:
  ```sh
  tools/cleanup-containers
  ```
  - Xóa các image openstack
  ```sh
  tools/cleanup-images
  ```



# Ref:
http://cshuo.top/2016/05/26/kolla-mitaka-ubuntu-14-04/
https://greatbsky.github.io/kolla-for-openstack-in-docker/en.html
http://egonzalez.org/openstack-kolla-deployment-from-rdo-packages/
http://ivan.chavero.com.mx/blog/doku.php/blog:installing_containerized_openstack_using_kolla
https://docs.openstack.org/developer/kolla-ansible/quickstart.html