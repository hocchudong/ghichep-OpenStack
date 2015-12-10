## Các ghi chép về OpenStack Neutron


### Cấu hình QoS cho Neutron trong OpenStack Liberty
-----

#### Bước 1: Cấu hình

#### Bước 2: Thực hiện test
##### Thực hiện trên Neutron Server 

- Tạo `qos-policy`
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

##### Link tham khảo
1. http://www.ajo.es/post/126667247769/neutron-qos-service-plugin
2. http://m.blog.csdn.net/blog/junheart/48373483
3 http://docs.openstack.org/networking-guide/adv_config_qos.html  (Cách tạo rule)

