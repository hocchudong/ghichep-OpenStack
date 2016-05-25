import swiftclient

auth_url = 'http://10.10.10.140:35357/v2.0'
username = raw_input('Nhap vao ten nguoi dung:')
password = raw_input('Nhap vao password: ')
print "\n"
print "-"*100
tenant = 'admin'
tenant_id = '11af54a847164d75b8b6ddad0e82c079'
region = 'RegionOne'
swift_conn = swiftclient.client.Connection(authurl=auth_url, user=username, key=password, tenant_name=tenant, auth_version='2.0', os_options={'tenant_id':tenant_id, 'region_name': region })

container_name = raw_input('Nhap vao ten container: ')
swift_conn.put_container(container_name)
print "\n"
print "-"*100
object_name = raw_input('nhap vao ten object: ')

data = raw_input ('nhap vao du lieu: ')
swift_conn.put_object(container_name, object_name, data)

link=raw_input('Nhap vao link dan den file: ')
contai=raw_input('Nhap vao ten container muon up doi tuong: ')
file_name=raw_input('Nhap vao ten file muon luu: ')
with open(link) as localfile:
	swift_conn.put_object(contai, file_name, localfile)