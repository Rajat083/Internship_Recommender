@echo off
echo Building PM Intern Recommender Docker image...
docker build -t pm-intern-recommender .

echo.
echo Running the container...
docker run -d ^
  --name pm-intern-recommender ^
  -p 8000:8000 ^
  -v "%cd%\Recommender\dataset:/app/Recommender/dataset:ro" ^
  -v "%cd%\Recommender\model:/app/Recommender/model:ro" ^
  pm-intern-recommender

echo.
echo Container started! API available at: http://localhost:8000
echo API documentation available at: http://localhost:8000/docs
echo.
echo To stop the container: docker stop pm-intern-recommender
echo To remove the container: docker rm pm-intern-recommender