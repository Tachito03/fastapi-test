from fastapi import FastAPI
from sqlalchemy import true
from routes.mailrelay import mails
from routes.heartrate import heart
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

#OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317"
#OTEL_EXPORTER_OTLP_HEADERS={'Authorization':'0d46ee25-4192-4164-91a7-4fe397ab31a7'}
OTEL_EXPORTER_OTLP_ENDPOINT="https://api.honeycomb.io"
OTEL_EXPORTER_OTLP_HEADERS={'x-honeycomb-team':'OQRB314TVAq3kyXQq2YssC'}


resource = Resource(attributes={SERVICE_NAME:"FastAPI"})
provider = TracerProvider(resource=resource)
#processor = BatchSpanProcessor(OTLPSpanExporter(endpoint='http://localhost:4317'))
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, headers=OTEL_EXPORTER_OTLP_HEADERS,insecure=True))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)



app = FastAPI(title='endPoints', 
              description='Primera versión de envio de mails, detalle de centros, calcúlo de frecuencia cardíaca ', 
              version='1.0.1', openapi_tags=[{
                  'name': 'fastAPI',
                  'description': 'endPoint Test'
              }])

app.include_router(mails)
app.include_router(heart)
LoggingInstrumentor().instrument()
FastAPIInstrumentor().instrument_app(app, tracer_provider=provider)

