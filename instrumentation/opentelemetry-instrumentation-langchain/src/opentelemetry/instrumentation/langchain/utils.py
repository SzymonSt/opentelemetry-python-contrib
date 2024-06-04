# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Callable, Dict, List, Optional

from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Tracer
from opentelemetry.trace.span import Span

RequestHookT = Optional[Callable[[Span, List, Dict], None]]
ResponseHookT = Optional[Callable[[Span, List, Dict], None]]

def _wrap_invoke(tracer: Tracer, request_hook: RequestHookT) -> Callable:
    def _traced_invoke(func, instance, args, kwargs):
        print("WHOLE ARGS: ", args)
        return func(*args, **kwargs)

    return _traced_invoke

def _wrap_response(tracer: Tracer, response_hook: ResponseHookT) -> Callable:
    def _traced_generate(func, instance, args, kwargs):
        print("WHOLE ARGS: ", args)
        return func(*args, **kwargs)

    return _traced_generate
