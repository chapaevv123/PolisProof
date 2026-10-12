FROM python:3.11-slim AS base
WORKDIR /app
ENV PYTHONPATH=/app/src PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY src ./src
COPY fixtures ./fixtures
COPY evaluation ./evaluation
COPY tests ./tests
RUN useradd --create-home --uid 10001 polisproof && chown -R polisproof:polisproof /app
USER polisproof

FROM base AS test
RUN python -m unittest discover -s tests -v

FROM base AS eval
RUN python evaluation/run_eval.py

FROM base AS runtime
ENV PORT=8080
EXPOSE 8080
CMD ["python", "-m", "polisproof.server", "--host", "0.0.0.0"]
