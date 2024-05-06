from django.shortcuts import render, redirect
from django.urls import reverse
# Create your views here.
from django.http import HttpResponseRedirect, JsonResponse
from .models import Goods, UploadedFile
from .forms import GoodsForm, UploadedFileForm
from django.views.decorators.csrf import csrf_exempt
import os
from alt_text import settings



# 메인화면(홈)
def main(request):
    main_list = Goods.objects.all()
    return render(request, 'home/main.html', {'main_list' : main_list})

def detail(request, goods_id):
    goods = Goods.objects.get(pk=goods_id)
    return render(request, 'home/detail.html', {'goods': goods})

@csrf_exempt
def upload(request):
    submitted = False
    goodsupload = None
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        # form = UploadedFileForm(request.POST)

        if form.is_valid():
            file_path = request.FILES['file_path']
            submitted = True
            
            # 업로드된 파일을 데이터베이스에 저장
            fileupload = UploadedFile(
                file_path=file_path
            )
            fileupload.save()

            # gpt_result = image_analysis(file_path.name)
            gpt_result = '이미지에는 고구마의 반쪽이 통으로 들어가 있는 모습이 보입니다.'
            # return redirect('review')
            
            goodsupload= Goods(
                image=fileupload,
                alt_text=gpt_result,
                name=file_path.name
            )
            goodsupload.save()

            # return redirect('review', goods_id=goodsupload.pk)
            return render(request, 'home/review.html', {
                'form': form,
                'submitted': submitted,
                'file_path': file_path.name,
                'gpt_result': gpt_result,
                'goodsupload':goodsupload
            })
    else:
        form = UploadedFileForm()
    return render(request, 'home/upload.html', {'form': form, 'submitted': submitted, 'goodsupload':goodsupload})

# def review(request, goods_id):
#     img_list = UploadedFile.objects.all()
#     goods = Goods.objects.get(image__id=goods_id)
#     if request.method == 'POST':
#         form = GoodsForm(request.POST, instance=goods)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             alt_text = form.cleaned_data['alt_text']

#             # 파일 업로드 처리
#             # ...

#             goods.name = name
#             goods.alt_text = alt_text
#             goods.save()
#     return render(request, 'home/review.html', {'img_list': img_list, 'name':name, 'alt_text': alt_text})

def review(request, goods_id):
    goods = Goods.objects.get(image__id=goods_id)

    if request.method == 'POST':
        # POST 요청이면 폼에서 제출된 데이터로 Goods 객체 업데이트
        goods.name = request.POST.get('name')
        goods.alt_text = request.POST.get('alt_text')
        goods.save()

    # 기존의 정보를 가져와서 HTML에 전달
    return redirect('home')
    # return render(request, 'home/review.html', {'goods': goods})


def image_analysis(file_path):
    import os,json
    import azure.ai.vision as sdk
    from openai import AzureOpenAI

    service_options = sdk.VisionServiceOptions(os.environ["VISION_ENDPOINT"],
                                            os.environ["VISION_KEY"])

    file = "/home/gh18477975/msproject/alt_text/uploads/" + file_path
    print("file, ",file)
    subject = file_path.split('.')[0]
    with open(file, 'rb') as f:
        image_buffer = f.read()

    image_source_buffer = sdk.ImageSourceBuffer()
    image_source_buffer.image_writer.write(image_buffer)
    vision_source = sdk.VisionSource(image_source_buffer=image_source_buffer)

    analysis_options = sdk.ImageAnalysisOptions()

    analysis_options.features = (
        sdk.ImageAnalysisFeature.DENSE_CAPTIONS |
        sdk.ImageAnalysisFeature.TEXT
    )

    analysis_options.language = "en"
    analysis_options.gender_neutral_caption = True

    image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options) # API 호출
    result = image_analyzer.analyze()
    text_li = []
    caption_li = []
    if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
        if result.dense_captions is not None:
            print(" Dense Captions:")
            
            for caption in result.dense_captions:
                print("   '{}', {}, Confidence: {:.4f}".format(caption.content, caption.bounding_box, caption.confidence))
                caption_li.append(caption.content)

        if result.text is not None:
            print(" Text:")
            
            for line in result.text.lines:
                points_string = "{" + ", ".join([str(int(point)) for point in line.bounding_polygon]) + "}"
                print("   Line: '{}', Bounding polygon {}".format(line.content, points_string))
                text_li.append(line.content)

    else:

        error_details = sdk.ImageAnalysisErrorDetails.from_result(result)
        print(" Analysis failed.")
        print("   Error reason: {}".format(error_details.reason))
        print("   Error code: {}".format(error_details.error_code))
        print("   Error message: {}".format(error_details.message))

    text_ext =  ' '.join(text_li)
    dic = {'caption' : caption_li, 'ocr' : text_ext }


    client = AzureOpenAI(
    # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
    api_version="2023-07-01-preview",
    # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
    azure_endpoint="",
    api_key = os.environ.get("AZURE_OPENAI_API_KEY"),

)

    completion = client.chat.completions.create(
    model="",  # e.g. gpt-35-instant
    messages=[
        {
            "role": "user",
            "content": """내가 넣은 정보는 딕셔너리야. caption 과 ocr 을 키로 가지고있어.
            caption 의 값에는 이미지 묘사, ocr의 값에는 이미지에서 뽑아낸 텍스트가 들어가있어.
            난 이 문장들을 종합하고 요약해 시각장애인에게 이미지를 설명해야하는 상황이야.
            넌 내가 같이 준 딕셔너리를 기반으로 대체텍스트를 만들어야해.

            이해하기 쉽게 예시를 알려줄께.
           input값으로, "{
                "caption": [
                "a group of boxes on a desk",
                "a close up of a box",
                "a blue and green box with white text",
                "a blue and white box with white text",
                "a close-up of a glass vase",
                "a blurry image of a banana"
            ],
            "ocr": "ILDONG 후디스 | 하이뮨 프로틴 밸런스 | 하이뮨 R 프로틴밸런스 간편하게 마시는 단백질 ILDONG 후디스 하이문 ILDONG 후디스 프로틴밸런스 하이문. 간편하게 마시는 단백질 프로틴밸런스 홍 동 · 식물성 6:4 균형 단백질 10 g 간편하게 마시는 단백질 ( 류신 1,000 mg / BCAA 1,500 mg ◇ 비타민 11종 / 미네랄 5종 9 동 · 식물성 6:4 균형 단백질 10 g 단백질 EM 류신 1,000 mg / BCAA 1,500 mg UP 비타민 11종 / 미네랄 5종 단백질 혼합음료 | 190 mL (165 kcal) UP 단백질 10g 혼합음료 | 190 mL (165 kcal) 단백질 10 g"
        }" 이 딕셔너리가 들어가면, caption 값 중에서 "a blue and green box with white text", "a blue and white box with white text", "a close up of a box"과 ocr 값의 ILDONG 후디스 하이뮨 프로틴 밸런스 라는 단백질 음료제품을 결합하여, 파란색과 흰색으로 디자인된 제품 박스가 "하이뮨 프로틴 밸런스"라는 단백질 음료가 보이는 거야. 또한, "ocr"의 값에서 류신, BCAA, 비타민, 미네랄, 단백질의 정확한 수치는 영양정보이기 때문에 그대로 설명해줘야해. 190mL(165kcal)는 "caption"에서 보이는 "a blue and green box with white text"의 박스의 용량과 칼로리인 것이야. 동,식물성 6 : 4 균형 이라는 "ocr"값은 풀어서 식물성과 동물성 단백질이 6:4의 균형을 이루고 있다고 설명해. "ocr"을 중심으로 이미지 내의 텍스트를 설명하고 난 후, "caption"을 한국어로 설명해.  그럼 결과값으로 다음처럼 나와야해. 

        output값으로, " 이 이미지에는 ILDONG 후디스 브랜드의 "하이뮨 프로틴 밸런스"라는 단백질 음료 제품이 보입니다. 제품 박스는 주로 파란색과 흰색으로 디자인되어 있으며, 박스의 중앙에는 '간편하게 마시는 단백질'이라는 문구가 있습니다. 각 박스에는 단백질 10g, 류신 1,000mg, BCAA 1,500mg이 포함되어 있으며, 비타민 11종과 미네랄 5종이 추가된 혼합음료라고 명시되어 있습니다. 박스의 하단에는 제품의 용량인 190mL와 칼로리가 165kcal임을 알려주는 정보가 있습니다. 이 제품들은 식물성과 동물성 단백질이 6:4의 균형을 이루고 있는 것으로 표기되어 있습니다.
        배경에는 책상 위에 놓인 것으로 보이는 물건들이 흐릿하게 보이며, 그 중에는 유리 화병과 바나나가 포함되어 있는 것 같습니다. 전반적으로 이 이미지는 단백질 보충을 위한 간편한 솔루션을 제공하는 식품 제품의 광고로 해석됩니다." 라는 결과값이 나와.

        자, 그럼 이 예시처럼하는데 예시는 절대로 따라하지마"""+ str(dic)+ """이 딕셔너리를 잘 설명하는 텍스트를 최종적으로 반드시 필요한 정보 3~5개를 중심으로 3문장내외로 만들어줘.
        단, 다음 조건은 반드시 지켜. 너의 대답에 ['OCR', '네', '알겠습니다', 'OCR 정보에 따르면', '대체텍스트'] 이 단어들과 내가 든 예시는 절대!!!!!!!!!!!!!!!!! 사용하지마.
""",
        },
    ],
)
    return completion.choices[0].message.content