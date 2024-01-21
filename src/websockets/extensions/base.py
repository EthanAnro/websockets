from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from .. import frames
from ..typing import ExtensionName, ExtensionParameter


__all__ = ["Extension", "ClientExtensionFactory", "ServerExtensionFactory"]


class Extension:
    """
    Base class for extensions.

    """

    name: ExtensionName
    """Extension identifier."""

    def decode(
        self,
        frame: frames.Frame,
        *,
        max_size: Optional[int] = None,
    ) -> frames.Frame:
        """
        Decode an incoming frame.

        Args:
            frame: Incoming frame.
            max_size: Maximum payload size in bytes.

        Returns:
            Decoded frame.

        Raises:
            PayloadTooBig: if decoding the payload exceeds ``max_size``.

        """
        raise NotImplementedError

    def encode(self, frame: frames.Frame) -> frames.Frame:
        """
        Encode an outgoing frame.

        Args:
            frame: Outgoing frame.

        Returns:
            Encoded frame.

        """
        raise NotImplementedError


class ClientExtensionFactory:
    """
    Base class for client-side extension factories.

    """

    name: ExtensionName
    """Extension identifier."""

    def get_request_params(self) -> List[ExtensionParameter]:
        """
        Build parameters to send to the server for this extension.

        Returns:
            Parameters to send to the server.

        """
        raise NotImplementedError

    def process_response_params(
        self,
        params: Sequence[ExtensionParameter],
        accepted_extensions: Sequence[Extension],
    ) -> Extension:
        """
        Process parameters received from the server.

        Args:
            params: Parameters received from the server for this extension.
            accepted_extensions: List of previously accepted extensions.

        Returns:
            An extension instance.

        Raises:
            NegotiationError: if parameters aren't acceptable.

        """
        raise NotImplementedError


class ServerExtensionFactory:
    """
    Base class for server-side extension factories.

    """

    name: ExtensionName
    """Extension identifier."""

    def process_request_params(
        self,
        params: Sequence[ExtensionParameter],
        accepted_extensions: Sequence[Extension],
    ) -> Tuple[List[ExtensionParameter], Extension]:
        """
        Process parameters received from the client.

        Args:
            params: Parameters received from the client for this extension.
            accepted_extensions: List of previously accepted extensions.

        Returns:
            To accept the offer, parameters to send to the client for this
            extension and an extension instance.

        Raises:
            NegotiationError: to reject the offer, if parameters received from
                the client aren't acceptable.

        """
        raise NotImplementedError
