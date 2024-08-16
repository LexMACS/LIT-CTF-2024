def recover_image(cropped, recovered):
    with open(cropped, 'rb') as f:
        data = f.read()

    iend_chunk = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'
    iend_position = data.find(iend_chunk) + len(iend_chunk)
    
    recovered_data = data[iend_position:]
    
    with open(recovered, 'wb') as f:
        f.write(recovered_data)

recover_image('image.png', 'recovered.png')
