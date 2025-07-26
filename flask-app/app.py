import logging
import time

from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

resource = Resource(attributes={
    SERVICE_NAME: "flask-app"
})

trace.set_tracer_provider(TracerProvider(resource=resource))

otlp_exporter = OTLPSpanExporter(  # 👈 DO NOT add 'insecure=True' here
    endpoint="http://tempo.monitoring.svc.cluster.local:4318/v1/traces"
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

@app.route("/")
def hello():
    return "Hello, traced world!"


@app.route("/work")
def work():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("db-call"):
        time.sleep(0.2)  # simulate DB call
    with tracer.start_as_current_span("internal-logic"):
        time.sleep(0.1)
    return "Did some work with nested spans!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)


