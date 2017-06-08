# Giới thiệu về kolla

Kolla là một trong 10 project lớn của Openstack với mục tiêu:
```sh
To provide production-ready containers and deployment tools for operating
OpenStack clouds.
```

Kolla cung cấp các images (là các OpenStack services và các thành phần hỗ trợ) cho docker containers, ansible playbook, Kubernetes template để deploy OpenStack.

#### Ý tưởng chính của kolla là:
- Các services như Keystone, glance, horizon, neutron,.... sẽ được chạy trên containers.
- Instance được tạo ra, sẽ chạy trên node compute giống với cài đặt như bình thường.

#### Ưu điểm khi sử dụng kolla:
- Đơn giản hóa việc triển khai OpenStack: nhanh chóng, dễ dàng.
- Dễ dàng mở rộng (scale), nâng cấp (upgrade) OpenStack.
- Chia nhỏ các services của OpenStack thành micro service (Docker containers). Mỗi micro service sẽ độc lập trong deployment, upgrading và scaling,...

#### Để dễ dàng trong việc tìm hiểu về kolla, các bạn nên có các kiến thức nền tảng sau:
- Ansible: https://github.com/hocchudong/ghichep-ansible
- Docker: https://github.com/hocchudong/ghichep-docker
- Kubernetes: https://github.com/hocchudong/ghichep-kubernetes

Kolla sẽ áp dụng các nền tảng công nghệ trên để thực hiện được mục tiêu của mình.

#### Có thể cài đặt Kolla với 2 phương pháp khác nhau:
- Cài đặt chạy các services openstack trên nền docker thuần.
- Cài đặt chạy các services openstack trên nền kubernetes sử dụng công nghệ containers là docker.