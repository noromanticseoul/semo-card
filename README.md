# QR 디지털 명함

QR을 찍으면 명함이 3D로 한 바퀴 돌고, 아래에 **연락처에 저장** 버튼이 뜨는 정적 웹페이지입니다.
서버 없이 GitHub Pages / Vercel / Netlify 어디든 올리면 됩니다.

## 파일 구성
| 파일 | 역할 |
|---|---|
| `card.json` | **내 정보는 여기만 고치면 됩니다** (이름, 전화, 이메일, 이미지 경로, 배포 주소) |
| `make.py` | `card.json` → `config.js`, `contact.vcf`, `qr.svg`, `qr.png` 자동 생성 |
| `index.html` | 명함 페이지 (3D 회전 애니메이션 + 버튼) |
| `assets/card-front.svg`, `card-back.svg` | 임시 명함 앞/뒷면 이미지 → 내 명함 이미지로 교체 |
| `vercel.json` | Vercel 배포 시 .vcf 파일 타입 지정 |

## 내 정보로 바꾸기
1. `card.json`의 이름·연락처를 수정합니다.
2. 명함 앞/뒷면 이미지(가로:세로 ≈ 1.75:1, 예: 1050×600 PNG/JPG)를 `assets/`에 넣고 `cardFront`, `cardBack` 경로를 바꿉니다.
3. (선택) 명함이 도는 **영상(mp4)** 을 직접 만들었다면 `cardVideo`에 경로를 넣으면 3D 카드 대신 영상이 재생됩니다. `backgroundVideo`에는 배경 영상을 넣을 수 있습니다.
4. 실행: `pip install segno && python3 make.py`

## 배포하고 QR 만들기
1. GitHub 저장소에 이 폴더를 올리고 Settings → Pages 에서 배포 (또는 Vercel에 폴더 드래그).
2. 나온 주소를 `card.json`의 `siteUrl`에 넣고 `python3 make.py`를 **다시 실행** → `qr.png`가 실제 주소로 바뀝니다.
3. `qr.png`를 종이 명함/스티커에 인쇄하면 끝.

## 연락처 저장 동작
- **아이폰(사파리)**: 버튼을 누르면 연락처 미리보기 화면이 뜨고 "새로운 연락처 생성"으로 저장.
- **안드로이드(크롬)**: `contact.vcf`가 내려받아지고, 알림/파일을 탭하면 연락처 앱으로 가져오기.
- 웹 정책상 사용자 확인 없이 연락처에 "자동" 저장하는 건 어떤 폰에서도 불가능해서, 버튼 한 번 + 저장 확인 한 번이 최소 단계입니다.
