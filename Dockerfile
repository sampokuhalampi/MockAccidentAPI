FROM python:3.12

RUN useradd -m appuser

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt && mkdir /app/instance && chown -R appuser:root /app

# Support arbitary Openshift uid 
# https://docs.openshift.com/container-platform/4.2/openshift_images/create-images.html#images-create-guide-openshift_create-images
RUN chgrp -R 0 /app && \
    chmod -R g=u /app
USER appuser

ENTRYPOINT ["python3", "-m"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
EXPOSE 5000
