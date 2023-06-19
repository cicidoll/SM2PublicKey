from InputProcess import InputProcess

def main() -> None:
    test = InputProcess()
    print(
        "\n转换完成，公钥信息如下： \nDer格式Base64编码公钥值：%s \nRaw格式Hex编码公钥值：%s"
        % (
            test.sm2_pubkey_info.pubkey.base64_der,
            test.sm2_pubkey_info.pubkey.hex_raw
        )
    )

if __name__ == "__main__":
    main()
    input("请输入任意操作结束程序")