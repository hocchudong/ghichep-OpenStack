## Các ghi chép về OpenStack Neutron


### Cấu hình QoS cho Neutron trong OpenStack Liberty
-----

#### Bước 1: Cấu hình
##### Trên Neutron Server

- Trong bản OpenStack Liberty thì Neutron nằm trên Controller
- Khai báo trong file `/etc/neutron/neutron.conf`
```sh
[DEFAULT]

service_plugins = router,qos

```

- Khai báo trong file `/etc/neutron/plugins/ml2/ml2_conf.ini` ở 2 section `[ml2]` và `[agent]`
```sh
[ml2]

extension_drivers = qos


[agent]

extensions = qos
```
##### Trên node COMPUTE
- Khai báo trong file `/etc/neutron/plugins/ml2/ml2_conf.ini` ở 2 section `[ml2]` và `[agent]`
```sh
[ml2]

extension_drivers = qos


[agent]

extensions = qos
```



#### Bước 2: Thực hiện test
Tạo 02 máy ảo để thực hiện test

##### Thực hiện trên Neutron Server 

- Tạo `qos-policy` có tên là `bw-limiter`
```sh
neutron qos-policy-create bw-limiter
```

- Setup bandwidth 
```sh
neutron qos-bandwidth-limit-rule-create --max-kbps 1000 --max-burst-kbps 100 bw-limiter
```

- Kiểm tra port trong neutron 
```sh
neutron port-list
```

- Áp rule vào port cần thiết lập
```sh
neutron port-update ID_PORT --qos-policy bw-limiter
```

- Bỏ rule của port vừa thiết lập
```sh
neutron port-update ID_PORT --no-qos-policy
```


- Đứng trên node compute kiểm tra port của máy ảo cần kiểm tra bằng lệnh
```sh
ovs-ctl show | grep qvo
```

- Ghi lại port cần kiểm tra và sử dụng lệnh nload ở dưới.
- Trên node compute thực hiện theo dõi bandwidth của máy ảo bằng lệnh nload 


- Thực hiện đẩy traffic vào máy cần kiểm tra (máy này có port được áp policy)
```sh
ssh cirros@$THE_IP_ADDRESS 'dd if=/dev/zero  bs=1M count=1000000000'
```



##### Link tham khảo
1. http://www.ajo.es/post/126667247769/neutron-qos-service-plugin
2. http://m.blog.csdn.net/blog/junheart/48373483
3 http://docs.openstack.org/networking-guide/adv_config_qos.html  (Cách tạo rule)

