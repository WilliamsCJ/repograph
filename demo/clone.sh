git clone https://github.com/tiangolo/fastapi.git
git clone https://github.com/RDFLib/pyLODE.git
git clone https://github.com/OmkarPathak/pygorithm.git

inspect4py -i pyLODE -o pyLODE-out -md -rm -si -ld -sc -r
inspect4py -i fastapi -o fastapi-out -md -rm -si -ld -sc -r
inspect4py -i pygorithm -o pygorithm-out -md -rm -si -ld -sc -r