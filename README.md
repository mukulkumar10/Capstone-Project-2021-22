## Capstone-Project 2021-22

# Proposed model
Medical Image Fusion using Deep Learning & Texture Features

### Requirements
- pytorch=0.4.1
- python=3.x
- torchvision
- numpy
- opencv-python
- jupyter notebook (suggested)
- anaconda (optional)

# Abstract
Analyzation of medical images is a tedious job for the radiologists to attain minute insights for proper diagnosis, one of the potential reasons being image artifacts with noise due to patient movement and faulty transmission. Multimodal Medical Image Fusion being an auxiliary approach assists doctors diagnose smoothly leveraging information enhancement technology, thus, solving the demarcated Statement Of Purpose (SOP). The primary objective of image fusion is to employ the complementary information in multiple images, to attain a higher resolution and intelligibility. In this project, our goal is to obtain a single image, which presents better performance under several popular evaluation criteria, by fusing two multi focused images of the same scene. Inspired by the framework of the transform-domain image fusion algorithms, the basic idea was to design a general image fusion framework based on the convolutional neural network (pre-trained architectures on ImageNet dataset) which should primarily contain 3 modules: feature extraction module, feature fusion module and image reconstruction/ regeneration module. We have employed Gray Level Co-Occurrence Matrix (GLCM) technique in order to bring the concept of “texture features” on the table which inherently acted as decision function (equivalently, a specific fusion rule among the rest) in the FUSION phase. Post auditioning several relevant fusion strategies, baseline hyper-parameter tunings, examining regeneration module of the architecture to inhibit minimal compensations post-fusion, feature-maps packaging, etc, the obtained sets of outputs were validated via a unified evaluation function (objective analysis in terms of standard metrics).



### Results
1. Zero Learning (VGG19 + Softmax Operator)
![Zero_Learning-Output](https://github.com/mukulkumar10/Capstone-Project-2021-22/blob/main/Results/Zero_Learning-Output.PNG)



2. IFCNN:
![Ifcnn-Output](https://github.com/mukulkumar10/Capstone-Project-2021-22/blob/main/Results/Ifcnn-Output.PNG)



3. IFCNN-GLCM-I
![Ifcnn-glcm-i-Output](https://github.com/mukulkumar10/Capstone-Project-2021-22/blob/main/Results/Ifcnn-glcm-i-Output.PNG)



4. IFCNN-GLCM-II
![Ifcnn-glcm-ii-Output](https://github.com/mukulkumar10/Capstone-Project-2021-22/blob/main/Results/Ifcnn-glcm-ii-Output.PNG)

5. IFCNN-SSIM
![Ifcnn_ssim-Output](https://github.com/mukulkumar10/Capstone-Project-2021-22/blob/main/Results/Ifcnn_ssim-Output.PNG)



6. FunFuseAn
![funfusean-Output](https://github.com/mukulkumar10/Capstone-Project-2021-22/blob/main/Results/funfusean-Output.PNG)



7. Textural Weighted Fusion (Proposed Model)
![Proposed_model_Output](https://github.com/mukulkumar10/Capstone-Project-2021-22/blob/main/Results/Proposed_model_Output.PNG)


### Citation
```
@article{zhang2020IFCNN,
  title={IFCNN: A General Image Fusion Framework Based on Convolutional Neural Network},
  author={Zhang, Yu and Liu, Yu and Sun, Peng and Yan, Han and Zhao, Xiaolin and Zhang, Li},
  journal={Information Fusion},
  volume={54},
  pages={99--118},
  year={2020},
  publisher={Elsevier}
}

@article{Fayez2019ZeroLearning,
  title={Zero Learning Fast Medical Image Fusion},
  author={Fayez Lahoud, Sabine Susstrunk},
  journal={International Conference on Information Fusion},
  volume={22},
  year={2019},
  publisher={IEEE}
}

```
