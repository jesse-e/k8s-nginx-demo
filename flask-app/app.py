import logging
import time

from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_current_span

# Set up logger
logger = logging.getLogger("my-app")
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Initialize Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Configure OpenTelemetry
resource = Resource(attributes={
    SERVICE_NAME: "flask-app"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(
    endpoint="http://tempo.monitoring.svc.cluster.local:4318/v1/traces"
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Utility function to log with trace ID
def log_with_trace_id(msg):
    span = get_current_span()
    ctx = span.get_span_context()
    trace_id = format(ctx.trace_id, "032x") if ctx and ctx.trace_id else "no-trace"
    logger.info(f"{msg} | trace_id={trace_id}")

@app.route("/")
def hello():
    log_with_trace_id("Serving hello endpoint")
    return "Hello, traced world!"

@app.route("/work")
def work():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("db-call"):
        log_with_trace_id("Starting db-call span")
        time.sleep(0.2)

    with tracer.start_as_current_span("internal-logic"):
        log_with_trace_id("Starting internal-logic span")
        time.sleep(0.1)

    log_with_trace_id("Finished /work endpoint")
    return "Did some work with nested spans!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
