# Cài đặt Kolla-kubernetes trên ubuntu 16.04

#### Các chú ý khi cài đặt
Tôi cài đặt vào khoảng thời gian giữa tháng 5, năm 2017. Kolla và Kubernetes luôn cập nhật công nghệ hằng ngày. Vì vậy, các bạn hãy theo dõi documents của kolla để nắm được chính xác nhất.

# 1. Mô hình
Mô hình tôi cài đặt:
- Chạy tất cả các service của openstack trên 1 node kubernetes.
- node chạy ubuntu 16.04, có địa chỉ card mạng là
```sh
ens3      Link encap:Ethernet  HWaddr 52:54:00:06:d9:c8  
          inet addr:172.16.69.237  Bcast:172.16.69.255  Mask:255.255.255.0
          inet6 addr: fe80::5054:ff:fe06:d9c8/64 Scope:Link


ens6      Link encap:Ethernet  HWaddr 52:54:00:e6:eb:79  
          inet addr:10.10.10.129  Bcast:10.10.10.255  Mask:255.255.255.0
          inet6 addr: fe80::5054:ff:fee6:eb79/64 Scope:Link
```

# 2. Các phiên bản phần mềm tôi cài đặt

```sh
ubuntu 16.04 LTS
docker = 1.12.6
helm = 2.3.0
kubectl = 1.6.2
kubeadm = 1.6.2
kubelet = 1.6.2
kubernetes-cni = 0.5.1
```

- Các yêu cầu về phần cứng
```sh
2 network interfaces
8GB main memory
40GB disk space
```


## 3.1 Deploy Kubernetes

- Tắt firewall
```sh
root@aio:~# ufw status
Status: inactive

root@aio:~# ufw disable
Firewall stopped and disabled on system startup
root@aio:~#
```

- Cài đặt kubernetes và docker
```sh
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo -E apt-key add -
cat <<EOF > kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF

sudo cp -aR kubernetes.list /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y docker.io kubeadm=1.6.2-00 kubectl=1.6.2-00 kubelet=1.6.2-00 kubernetes-cni=0.5.1-00
sudo systemctl enable docker
sudo systemctl start docker
sudo systemctl enable kubelet
```

- Enable CGROUP driver:
```sh
CGROUP_DRIVER=$(sudo docker info | grep "Cgroup Driver" | awk '{print $3}')
sudo sed -i "s|KUBELET_KUBECONFIG_ARGS=|KUBELET_KUBECONFIG_ARGS=--cgroup-driver=$CGROUP_DRIVER |g" /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
```

- Cài đặt ip DNS kubernetes
```sh
sudo sed -i 's/10.96.0.10/10.3.3.10/g' /etc/systemd/system/kubelet.service.d/10-kubeadm.conf

systemctl daemon-reload
systemctl start docker
systemctl restart kubelet
```

- Deploy Kubernetes với kubeadm
```sh
sudo kubeadm init --pod-network-cidr=10.1.0.0/16 --service-cidr=10.3.3.0/24
```

- Load các thông tin kubedm vào hệ thống
```sh
mkdir -p $HOME/.kube
sudo -H cp /etc/kubernetes/admin.conf $HOME/.kube/config
sudo -H chown $(id -u):$(id -g) $HOME/.kube/config
```

- Deploy Canal CNI driver (network)
```sh
curl -L https://raw.githubusercontent.com/projectcalico/canal/master/k8s-install/1.6/rbac.yaml -o rbac.yaml
kubectl apply -f rbac.yaml

curl -L https://raw.githubusercontent.com/projectcalico/canal/master/k8s-install/1.6/canal.yaml -o canal.yaml
sed -i "s@10.244.0.0/16@10.1.0.0/16@" canal.yaml
kubectl apply -f canal.yaml
```

- Untaint the node (Cho phép lập lịch và chạy pods trên ngay node master của kubernetes)
```sh
kubectl taint nodes --all=true  node-role.kubernetes.io/master:NoSchedule-
```

- Quá trình cài đặt kubernetes đã hoàn tất. Hãy kiểm tra.
```sh
root@aio:~# kubectl get pods --namespace=kube-system
NAME                             READY     STATUS    RESTARTS   AGE
canal-cn5l3                      3/3       Running   0          10d
canal-k9858                      3/3       Running   3          10d
etcd-master                      1/1       Running   11         10d
kube-apiserver-master            1/1       Running   1          10d
kube-controller-manager-master   1/1       Running   2          10d
kube-dns-3913472980-31dzr        3/3       Running   0          10d
kube-proxy-18796                 1/1       Running   0          10d
kube-scheduler-master            1/1       Running   7          10d
root@aio:~# 
```

## 3.2 Deploy kolla-Kubernetes

- Ghi đè các cài đặt RBAC:
```sh
kubectl update -f <(cat <<EOF
apiVersion: rbac.authorization.k8s.io/v1alpha1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: Group
  name: system:masters
- kind: Group
  name: system:authenticated
- kind: Group
  name: system:unauthenticated
EOF
)
```

- Cài đặt Helm:
```sh
curl -L https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get > get_helm.sh
chmod 700 get_helm.sh
./get_helm.sh
helm init
```

```sh
root@aio:~# helm version
Client: &version.Version{SemVer:"v2.3.0", GitCommit:"d83c245fc324117885ed83afc90ac74afed271b4", GitTreeState:"clean"}
Server: &version.Version{SemVer:"v2.3.0", GitCommit:"d83c245fc324117885ed83afc90ac74afed271b4", GitTreeState:"clean"}
```

- Cài đặt các gói cần thiết
```sh
apt-get install -y software-properties-common ansible python-pip python-dev git gcc libffi-dev openssl crudini
pip install -U pip
apt-get install -y ntp
systemctl enable ntp
systemctl start ntp
pip install python-openstackclient
pip install python-neutronclient
pip install python-cinderclient
```

- Clone kolla-ansible and kolla-Kubernetes
```sh
mkdir kolla-bringup
cd kolla-bringup
git clone http://github.com/openstack/kolla-ansible
git clone http://github.com/openstack/kolla-kubernetes
```

- Cài đặt kolla-ansible and kolla-kubernetes
```sh
sudo pip install -U kolla-ansible/ kolla-kubernetes/
```

- Copy default Kolla configuration to /etc:
```sh
sudo cp -aR /usr/local/share/kolla-ansible/etc_examples/kolla /etc
```

- Copy default kolla-kubernetes configuration to /etc:
```sh
sudo cp -aR kolla-kubernetes/etc/kolla-kubernetes /etc
```

- Tạo default password:
```sh
sudo kolla-kubernetes-genpwd
```

- Tạo Kubernetes namespace để cô lập môi trường Kolla:
```sh
kubectl create namespace kolla
```

- Label the AIO node as the compute and controller node:
```sh
kubectl label node $(hostname) kolla_compute=true
kubectl label node $(hostname) kolla_controller=true
```

- Chỉnh sửa file Cấu hình  `/etc/kolla/globals.yml`:
```sh
1. Set `network_interface` in `/etc/kolla/globals.yml` to the
   Management interface name. E.g: `eth0`.
2. Set `neutron_external_interface` in `/etc/kolla/globals.yml` to the
   Neutron interface name. E.g: `eth1`. This is the external
   interface that Neutron will use.  It must not have an IP address
   assigned to it.
```

- Thêm đoạn sau vào file `/etc/kolla/globals.yml`
```sh
cat <<EOF > add-to-globals.yml
kolla_base_distro: "ubuntu"
kolla_install_type: "source"
tempest_image_alt_id: "{{ tempest_image_id }}"
tempest_flavor_ref_alt_id: "{{ tempest_flavor_ref_id }}"

neutron_plugin_agent: "openvswitch"
api_interface_address: 0.0.0.0
tunnel_interface_address: 0.0.0.0
orchestration_engine: KUBERNETES
memcached_servers: "memcached"
keystone_admin_url: "http://keystone-admin:35357/v3"
keystone_internal_url: "http://keystone-internal:5000/v3"
keystone_public_url: "http://keystone-public:5000/v3"
glance_registry_host: "glance-registry"
neutron_host: "neutron"
keystone_database_address: "mariadb"
glance_database_address: "mariadb"
nova_database_address: "mariadb"
nova_api_database_address: "mariadb"
neutron_database_address: "mariadb"
cinder_database_address: "mariadb"
ironic_database_address: "mariadb"
placement_database_address: "mariadb"
rabbitmq_servers: "rabbitmq"
openstack_logging_debug: "True"
enable_haproxy: "no"
enable_heat: "no"
enable_cinder: "yes"
enable_cinder_backend_lvm: "yes"
enable_cinder_backend_iscsi: "yes"
enable_cinder_backend_rbd: "no"
enable_ceph: "no"
enable_elasticsearch: "no"
enable_kibana: "no"
glance_backend_ceph: "no"
cinder_backend_ceph: "no"
nova_backend_ceph: "no"
EOF
cat ./add-to-globals.yml | sudo tee -a /etc/kolla/globals.yml
```

- enable QEMU libvirt:
```sh
sudo mkdir /etc/kolla/config
sudo tee /etc/kolla/config/nova.conf<<EOF
[libvirt]
virt_type=qemu
cpu_mode=none
EOF
```

- Tạo default config cho các service:
```sh
sudo kolla-ansible genconfig
```

- Tạo Kubernetes secrets và chèn vào Kubernetes:
```sh
kolla-kubernetes/tools/secret-generator.py create
```

- Tạo  Kolla config maps:
```sh
kollakube res create configmap \
    mariadb keystone horizon rabbitmq memcached nova-api nova-conductor \
    nova-scheduler glance-api-haproxy glance-registry-haproxy glance-api \
    glance-registry neutron-server neutron-dhcp-agent neutron-l3-agent \
    neutron-metadata-agent neutron-openvswitch-agent openvswitch-db-server \
    openvswitch-vswitchd nova-libvirt nova-compute nova-consoleauth \
    nova-novncproxy nova-novncproxy-haproxy neutron-server-haproxy \
    nova-api-haproxy cinder-api cinder-api-haproxy cinder-backup \
    cinder-scheduler cinder-volume iscsid tgtd keepalived \
    placement-api placement-api-haproxy
```

- Enable resolv.conf:
```sh
kolla-kubernetes/tools/setup-resolv-conf.sh kolla
```

- Build all Helm microcharts, service charts, and metacharts:
```sh
kolla-kubernetes/tools/helm_build_all.sh .
```

- Tạo file cloud.yaml file để cấu hình các charts của helm:
```sh
cat <<EOF > cloud.yaml
global:
   kolla:
     all:
       docker_registry: docker.io
       image_tag: "4.0.0"
       kube_logger: false
       external_vip: "192.168.7.105"
       base_distro: "ubuntu"
       install_type: "source"
       tunnel_interface: "docker0"
       resolve_conf_net_host_workaround: true
     keystone:
       all:
         admin_port_external: "true"
         dns_name: "192.168.7.105"
       public:
         all:
           port_external: "true"
     rabbitmq:
       all:
         cookie: 67
     glance:
       api:
         all:
           port_external: "true"
     cinder:
       api:
         all:
           port_external: "true"
       volume_lvm:
         all:
           element_name: cinder-volume
         daemonset:
           lvm_backends:
           - '192.168.7.105': 'cinder-volumes'
     ironic:
       conductor:
         daemonset:
           selector_key: "kolla_conductor"
     nova:
       placement_api:
         all:
           port_external: true
       novncproxy:
         all:
           port: 6080
           port_external: true
     openvwswitch:
       all:
         add_port: true
         ext_bridge_name: br-ex
         ext_interface_name: enp1s0f1
         setup_bridge: true
     horizon:
       all:
         port_external: true
EOF
```

Trong đó: 
`YOUR_NETWORK_INTERFACE_ADDRESS_FROM_GLOBALS.YML`: địa chỉ card mạng trao đổi với các service trong openstack.

`YOUR_NEUTRON_INTERFACE_NAME_FROM_GLOBALS.YML`: Tên card mạng ra bên ngoài

`YOUR_NETWORK_INTERFACE_NAME_FROM_GLOBALS.YML`: Tên card mạng trao đổi với các service trong openstack.

Chỉnh sửa các thông số trên vào file `cloud.yaml`:

```sh
sed -i "s@192.168.7.105@YOUR_NETWORK_INTERFACE_ADDRESS_FROM_GLOBALS.YML@g" ./cloud.yaml
```


```sh
sed -i "s@enp1s0f1@YOUR_NEUTRON_INTERFACE_NAME_FROM_GLOBALS.YML@g" ./cloud.yaml
```

```sh
sed -i "s@docker0@YOUR_NETWORK_INTERFACE_NAME_FROM_GLOBALS.YML@g" ./cloud.yaml
```

- Tạo service mariadb:
```sh
helm install --debug kolla-kubernetes/helm/service/mariadb --namespace kolla --name mariadb --values ./cloud.yaml
```

- Sau khi mariadb chạy xong, tiếp tục tạo các service khác:
```sh
helm install --debug kolla-kubernetes/helm/service/rabbitmq --namespace kolla --name rabbitmq --values ./cloud.yaml
helm install --debug kolla-kubernetes/helm/service/memcached --namespace kolla --name memcached --values ./cloud.yaml
helm install --debug kolla-kubernetes/helm/service/keystone --namespace kolla --name keystone --values ./cloud.yaml
helm install --debug kolla-kubernetes/helm/service/glance --namespace kolla --name glance --values ./cloud.yaml
helm install --debug kolla-kubernetes/helm/service/cinder-control --namespace kolla --name cinder-control --values ./cloud.yaml
helm install --debug kolla-kubernetes/helm/service/horizon --namespace kolla --name horizon --values ./cloud.yaml
helm install --debug kolla-kubernetes/helm/service/openvswitch --namespace kolla --name openvswitch --values ./cloud.yaml
helm install --debug kolla-kubernetes/helm/service/neutron --namespace kolla --name neutron --values ./cloud.yaml
helm install --debug kolla-kubernetes/helm/service/nova-control --namespace kolla --name nova-control --values ./cloud.yaml
helm install --debug kolla-kubernetes/helm/service/nova-compute --namespace kolla --name nova-compute --values ./cloud.yaml
```

- Sau khi `nova-compute` chạy xong, tạo các service sau:
```sh
helm install --debug kolla-kubernetes/helm/microservice/nova-cell0-create-db-job --namespace kolla --name nova-cell0-create-db-job --values ./cloud.yaml
helm install --debug kolla-kubernetes/helm/microservice/nova-api-create-simple-cell-job --namespace kolla --name nova-api-create-simple-cell --values ./cloud.yaml
```

- Quá trình dựng các service đã xong, để kiểm tra, ta chạy lệnh sau:
```sh
watch -d kubectl get pods --all-namespaces
```
```sh
Every 2.0s: kubectl get pods --namespace=kolla                                                                                                                         Mon May 29 15:10:09 2017

NAME                                      READY     STATUS    RESTARTS   AGE                                                                                                                   
cinder-api-2866011699-bw44v               2/3       Running   3          10d                                                                                                                   
cinder-scheduler-0                        1/1       Running   1          10d                                                                                                                   
cinder-volume-qwtkf                       1/1       Running   6          9d                                                                                                                    
glance-api-1989953154-1jrt3               1/1       Running   1          10d                                                                                                                   
glance-registry-1123305651-p55d0          3/3       Running   3          10d                                                                                                                   
horizon-3458108456-zwbm6                  1/1       Running   1          10d                                                                                                                   
iscsid-v78jq                              1/1       Running   44         9d                                                                                                                    
keystone-1902127961-0hhh8                 1/1       Running   1          9d                                                                                                                    
keystone-1902127961-53hdv                 1/1       Running   1          9d                                                                                                                    
keystone-1902127961-clswk                 1/1       Running   1          9d                                                                                                                    
mariadb-0                                 1/1       Running   0          4d                                                                                                                    
memcached-3907143468-0bd10                2/2       Running   2          10d                                                                                                                   
neutron-dhcp-agent-7kh05                  1/1       Running   1          9d                                                                                                                    
neutron-l3-agent-network-9vnk4            1/1       Running   1          9d                                                                                                                    
neutron-metadata-agent-network-kjtpb      1/1       Running   1          9d                                                                                                                    
neutron-openvswitch-agent-network-nk8bc   1/1       Running   1          9d                                                                                                                    
neutron-server-2416758762-r9q1k           2/3       Running   3          9d                                                                                                                    
nova-api-4039243040-9f4c3                 2/3       Running   3          9d                                                                                                                    
nova-compute-0ltbw                        1/1       Running   0          9d                                                                                                                    
nova-conductor-0                          1/1       Running   1          9d                                                                                                                    
nova-consoleauth-0                        1/1       Running   1          9d                                                                                                                    
nova-libvirt-dh88r                        1/1       Running   0          9d                                                                                                                    
nova-novncproxy-1896700624-d6tpx          3/3       Running   3          9d                                                                                                                    
nova-scheduler-0                          1/1       Running   1          9d                                                                                                                    
openvswitch-ovsdb-network-j2v8p           1/1       Running   1          10d                                                                                                                   
openvswitch-vswitchd-network-kspvt        1/1       Running   1          10d                                                                                                                   
placement-api-1605503990-3q99l            1/1       Running   1          9d                                                                                                                    
rabbitmq-0                                1/1       Running   1          9d                                                                                                                    
tgtd-pstc0                                1/1       Running   1          10d   
```

- Generate openrc file:
```sh
kolla-kubernetes/tools/build_local_admin_keystonerc.sh ext
source ~/keystonerc_admin
```

- Bootstrap the cloud environment and create a VM as requested:
```sh
kolla-ansible/tools/init-runonce
```

- Create a floating IP address and add to the VM:
```sh
openstack server add floating ip demo1 $(openstack floating ip create public1 -f value -c floating_ip_address)
```

- Đến đây, quá trình dựng openstack đã xong. Để kiểm tra các service ta có thể dùng các lệnh sau:
```sh
root@aio:~# kubectl get svc -n kolla
NAME                 CLUSTER-IP       EXTERNAL-IP     PORT(S)     AGE
cinder-api           172.16.128.132   172.16.69.237   8776/TCP    10d
glance-api           172.16.128.59    172.16.69.237   9292/TCP    10d
glance-registry      172.16.128.89    <none>          9191/TCP    10d
horizon              172.16.128.109   172.16.69.237   80/TCP      10d
keystone-admin       172.16.128.140   172.16.69.237   35357/TCP   10d
keystone-internal    172.16.128.42    <none>          5000/TCP    10d
keystone-public      172.16.128.144   172.16.69.237   5000/TCP    10d
mariadb              172.16.128.25    <none>          3306/TCP    10d
memcached            172.16.128.2     <none>          11211/TCP   10d
neutron-server       172.16.128.115   172.16.69.237   9696/TCP    9d
nova-api             172.16.128.4     172.16.69.237   8774/TCP    9d
nova-metadata        172.16.128.159   <none>          8775/TCP    9d
nova-novncproxy      172.16.128.45    172.16.69.237   6080/TCP    9d
nova-placement-api   172.16.128.61    172.16.69.237   8780/TCP    9d
rabbitmq             172.16.128.40    <none>          5672/TCP    9d
rabbitmq-mgmt        172.16.128.124   <none>          15672/TCP   9d
root@aio:~# 
```

```sh
root@aio:~# kubectl get configmap -n kube-system
NAME                                 DATA      AGE
canal-config                         4         10d
cinder-control.v1                    1         10d
cinder-volume-lvm.v1                 1         10d
extension-apiserver-authentication   6         10d
glance.v1                            1         10d
horizon.v1                           1         10d
keystone.v1                          1         10d
kube-proxy                           1         10d
mariadb.v1                           1         10d
memcached.v1                         1         10d
neutron.v1                           1         9d
nova-api-create-simple-cell.v1       1         9d
nova-cell0-create-db-job.v1          1         9d
nova-compute.v1                      1         9d
nova-control.v1                      1         9d
openvswitch.v1                       1         10d
rabbitmq.v1                          1         9d
```

```sh
root@aio:~# kubectl get deployments --all-namespaces
NAMESPACE     NAME              DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kolla         cinder-api        1         1         1            0           10d
kolla         glance-api        1         1         1            1           10d
kolla         glance-registry   1         1         1            1           10d
kolla         horizon           1         1         1            1           10d
kolla         keystone          3         3         3            3           10d
kolla         memcached         1         1         1            1           10d
kolla         neutron-server    1         1         1            0           9d
kolla         nova-api          1         1         1            0           9d
kolla         nova-novncproxy   1         1         1            1           9d
kolla         placement-api     1         1         1            1           9d
kube-system   kube-dns          1         1         1            0           10d
kube-system   tiller-deploy     1         1         1            0           10d
root@aio:~# 
```

#### Truy cập dashboard OpenStack
- Lấy địa chỉ ip:
```sh
root@aio:~# kubectl get svc horizon --namespace=kolla
NAME      CLUSTER-IP       EXTERNAL-IP     PORT(S)   AGE
horizon   172.16.128.109   172.16.69.237   80/TCP    10d
```

- Đọc thông tin user và password từ keystone
```sh
$ cat ~/keystonerc_admin | grep OS_USERNAME
export OS_USERNAME=admin

$ cat ~/keystonerc_admin | grep OS_PASSWORD
export OS_PASSWORD=tbwy6otptly7waSV0n195YeejC5fLDJK2HfKkmhx
```

- Truy cập dashboard bằng địa chỉ ip với thông tin username và password ở trên.

# Tài liệu tham khảo
- https://docs.openstack.org/developer/kolla-kubernetes/deployment-guide.html