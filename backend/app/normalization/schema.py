from typing import Any

from pydantic import BaseModel, Field


class SourceInfo(BaseModel):
    vendor: str | None = None
    product: str | None = None
    type: str | None = None


class NetworkEndpoint(BaseModel):
    ip: str | None = None
    port: int | None = None


class NetworkInfo(BaseModel):
    source: NetworkEndpoint = Field(default_factory=NetworkEndpoint)
    destination: NetworkEndpoint = Field(default_factory=NetworkEndpoint)
    protocol: str | None = None


class EventInfo(BaseModel):
    category: str | None = None
    type: str | None = None
    action: str | None = None
    severity: str | int | None = None


class RawInfo(BaseModel):
    payload: str
    format: str
    sha256: str


class TraceabilityInfo(BaseModel):
    raw_event_id: str
    parser: str
    parser_version: str


class UniversalEvent(BaseModel):
    event_id: str
    timestamp: str | None = None

    source: SourceInfo = Field(default_factory=SourceInfo)

    event: EventInfo = Field(default_factory=EventInfo)

    network: NetworkInfo = Field(default_factory=NetworkInfo)

    raw: RawInfo

    traceability: TraceabilityInfo