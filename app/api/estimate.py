# MVC에서 Controller 역할을 하는 모듈
from fastapi import APIRouter, File, UploadFile
from app.service import estimate_service
from fastapi import File, UploadFile, Form
from typing import List
import json
import os

router = APIRouter()

@router.get("/test", response_model=dict)
async def test() :
    return {"status": "ok", "message": "Send Image to FastAPI successfully"}


# Spring Boot => FastAPI MultipartFile(이미지 파일) 전달
@router.post("/estimate", response_model=dict)
async def upload_file(files: List[UploadFile] = File(...), filePathList: List[str] = Form(...)) :
    # 문자열로 전달되어 리스트로 변환
    filePathList = json.loads(filePathList[0])
    
    idx = 0
    
    saved_files = []
    
    for filePath in filePathList : 
        save_path = "app/uploads/" + filePath[0:8]
        
        # 날짜 폴더 생성
        os.makedirs(save_path, exist_ok=True)  
        
        # 파일 읽기
        content = await files[idx].read()
        
        # 저장 경로 설정
        save_path = os.path.join(save_path, filePath)

        with open(save_path, "wb") as f:
            f.write(content)
        
        # 후처리 작업에 필요한 사용자 정의 객체
        saved_files.append({
            "save_path" : save_path,
            "filename": files[idx].filename,
            "filepath" : filePath,
            "size": len(content)
        })
        
        idx+=1
        
    
    # 서비스 계층 호출
    estimate_service.estimate_custom_vision(saved_files)
    
    # schemas 모델 객체 -> Spring Boot 응답
    return {"status": "ok", "message": "Send Image to FastAPI successfully"}
