# concourse-datadog-tracing
Concourse is able to direct [traces natively to Jaegger](https://concourse-ci.org/tracing.html) - how though would you be able to integrate with a [Datadog agent](https://docs.datadoghq.com/api/v1/tracing/)?

Opencensus is a project that offers [agents\collectors](https://opencensus.io/service/components/agent/) that can receive traces from a variety of [sources](https://opencensus.io/service/receivers/) and [export](https://opencensus.io/service/exporters/) them to a variety of backends (this project has since been merged with OpenTracing into the OpenTelemetry project).

Assumption:

We're deploying both Concourse and the Datadog agents on K8s

### Configuring Concourse

You'll have to modify the Concourse Worker with the following additions\modification to the ENV variables.

We'll use the downward API to reference the node the worker is deployed on. This pod will end up communicating with the Opencensus Agent.

```
- name: HOST_IP
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: status.hostIP
    - name: CONCOURSE_TRACING_JAEGER_ENDPOINT
      value: http://$(HOST_IP):14268/api/traces
```

### Configuring Datadog agent

1) You'll have to enable APM: https://docs.datadoghq.com/agent/kubernetes/apm/?tab=helm

This allows the Datadog agent to listent for events\traces on port 8126.

2) On the trace-agent init container you'll have to make the 8126 port a hostPort. This is so that Opencensus agent can traces to the agent via localhost:8126

```
        ports:
        - containerPort: 8126
          hostPort: 8126
          name: traceport
          protocol: TCP
```

### Configuring the OpenCensus Agent

You can use the referenced agent.yaml to deploy the OpenCensus agent. It'll deploy the daemonset and runs an init container that creates the config map (based on the nodes IP) and mounts it into the OpenCensus agent.


