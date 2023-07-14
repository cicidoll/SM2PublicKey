from InputProcess import InputProcess

def main() -> None:
    try:
        input_process = InputProcess()
        print(
            "\n转换完成，公钥信息如下： \nDer格式Base64编码公钥值：\n%s \nRaw格式Hex编码公钥值：\n%s"
            % (
                input_process.sm2_pubkey_info.pubkey.base64_der,
                input_process.sm2_pubkey_info.pubkey.hex_raw
            )
        )
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
    input("\n请输入任意操作结束程序")