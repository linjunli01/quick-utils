from modbus_tcp import ModbusTcp


def to_test_all():
    # 加载配置
    config = {
        '1': {

        },
        'modbus': {

        }
    }
    modbus_config = config['modbus']
    hosts = ['127.0.0.1', '127.0.0.1', '127.0.0.1']
    port = [502, 503, 504]
    import traceback
    try:
        with ModbusTcp(host=hosts[0], port=port[0]) as c1, ModbusTcp(host=hosts[1], port=port[1]) as c2, ModbusTcp(
                host=hosts[2],
                port=port[2]) as c3:
            print('connect to all modbus tcp')
            print(
                '--------------------------------------------------------------------------------------------------------------------------------------------------------')
            c_map = {
                '1': c1,
                '2': c2,
                '3': c3
            }

            for i in config.keys():
                if i != 'modbus':
                    salve_data = config[i]
                    print(f"'{salve_data['tcp_id']}'")
                    client = c_map[str(salve_data['tcp_id'])]
                    ready_sig = client.read(slave_id=salve_data['slave_id'], addr=salve_data['ready'], quantity=1)
                    # 写入准备信号
                    ready_res = client.write(slave_id=salve_data['slave_id'], addr=salve_data['ready'], val=2)
                    print(
                        '--------------------------------------------------------------------------------------------------------------------------------------------------------')
    except Exception as e:
        print(traceback.format_exc())


if __name__ == '__main__':
    to_test_all()
