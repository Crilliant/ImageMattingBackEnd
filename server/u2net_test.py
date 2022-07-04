import os
import torch
from torch.autograd import Variable
from torchvision import transforms
from PIL import Image
from server.data_loader import RescaleT, ToTensorLab, SalObjData
from server.model import U2NETP
import numpy as np


# normalize the predicted SOD probability map
def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)

    dn = (d - mi) / (ma - mi)
    # for i in range(dn.shape[1] - 1):
    #    for j in range(dn.shape[2] - 1):
    #        if dn[0][i][j] > 0.5:
    #            dn[0][i][j] = 1
    #        else:
    #            dn[0][i][j] = 0

    return dn


def save_output(image_path, pred, d_dir, shape):
    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()

    im = Image.fromarray(predict_np * 255).convert('RGB')

    imo = im.resize((shape[1], shape[0]), resample=Image.BILINEAR)

    pure_img_name = os.path.basename(image_path)
    pure_img_name = pure_img_name.split('.')[-2] + ".png"

    imo.save(d_dir + "/" + pure_img_name)


def get_mask(pred, shape):
    predict = pred
    predict = predict.squeeze()
    predict_np = predict.cpu().data.numpy()

    im = Image.fromarray(predict_np * 255).convert('L')
    imo = im.resize((shape[1], shape[0]), resample=Image.BILINEAR)

    return np.array(imo)


# 单张图片，生成掩码png
def inference_img(img_path, save_dir):
    # --------- 1. get image path and name ---------
    model_name = 'u2netp'

    model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saved_models', model_name,
                             model_name + '.pth')
    print(img_path)

    # --------- 2. dataloader ---------
    # 1. dataloader
    salobj_data = SalObjData(img_path=img_path,
                             transform=transforms.Compose([RescaleT(320),
                                                           ToTensorLab(flag=0)])
                             )

    # --------- 3. model define ---------
    print("...load U2NEP---4.7 MB")
    net = U2NETP(3, 1)

    if torch.cuda.is_available():
        print("use cuda")
        net.load_state_dict(torch.load(model_dir))
        print("load successfully!")
        net.cuda()
    else:
        net.load_state_dict(torch.load(model_dir, map_location='cpu'))
    net.eval()

    # --------- 4. inference for each image ---------
    print("inferencing:", img_path)

    inputs_test, _, image_shape = salobj_data.get()
    inputs_test = inputs_test.unsqueeze(dim=0)
    inputs_test = inputs_test.type(torch.FloatTensor)

    if torch.cuda.is_available():
        inputs_test = Variable(inputs_test.cuda())
    else:
        inputs_test = Variable(inputs_test)

    # RuntimeError: CuDNN error: CUDNN_STATUS_INTERNAL_ERROR
    torch.backends.cudnn.benchmark = False
    d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)

    # normalization
    pred = d1[:, 0, :, :]
    pred = normPRED(pred)  # 概率均匀映射到[0, 1]

    # save_output(img_path, pred, save_dir, image_shape)
    del d1, d2, d3, d4, d5, d6, d7
    return get_mask(pred, image_shape)


if __name__ == "__main__":
    # torch.backends.cudnn.benchmark = True
    inference_img(r'E:\Code\ImageMatting\BackEnd\server\test_data/test_images/alask.png',
                  r'E:\Code\ImageMatting\BackEnd\server\test_data\mytest')
