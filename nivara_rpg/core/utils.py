from __future__ import annotations

from typing import TYPE_CHECKING, Any, overload

from discord import Embed
from discord.utils import MISSING

from data.constants.core import ERROR_COLOUR, PRIMARY_COLOUR

if TYPE_CHECKING:
    from typing import Any, TypeGuard, TypeVar

    from discord import (
        AllowedMentions,
        Attachment,
        File,
        Interaction,
        WebhookMessage,
    )
    from discord.abc import Snowflake
    from discord.ui.view import View

    T = TypeVar("T")


async def safe_edit_response(
    interaction: Interaction,
    *,
    content: str | None = MISSING,
    embeds: list[Embed] = MISSING,
    embed: Embed | None = MISSING,
    file: File = MISSING,
    files: list[File] = MISSING,
    attachments: list[Attachment] = MISSING,
    view: View | None = MISSING,
    allowed_mentions: AllowedMentions | None = None,
    thread: Snowflake | None = MISSING,
    suppress: bool = False,
) -> None | WebhookMessage | Interaction:
    """|coro|

    Attempts to edit the original message if possible. Otherwise sends a new message
    all the while responding to the interaction.

    Parameters
    ----------
    message_id: :class:`int`
        The message ID to edit.
    content: Optional[:class:`str`]
        The content to edit the message with or ``None`` to clear it.
    embeds: List[:class:`Embed`]
        A list of embeds to edit the message with.
    embed: Optional[:class:`Embed`]
        The embed to edit the message with. ``None`` suppresses the embeds.
        This should not be mixed with the ``embeds`` parameter.
    attachments: List[:class:`Attachment`]
        A list of attachments to keep in the message. If ``[]`` is passed
        then all attachments are removed.
    file: :class:`File`
        The file to upload. This cannot be mixed with ``files`` parameter.
    files: List[:class:`File`]
        A list of files to send with the content. This cannot be mixed with the
        ``file`` parameter.
    allowed_mentions: :class:`AllowedMentions`
        Controls the mentions being processed in this message.
        See :meth:`.abc.Messageable.send` for more information.
    view: Optional[:class:`~discord.ui.View`]
        The updated view to update this message with. If ``None`` is passed then
        the view is removed. The webhook must have state attached, similar to
        :meth:`send`.
    thread: Optional[:class:`~discord.abc.Snowflake`]
        The thread that contains the message.
    suppress: :class:`bool`
        Whether to suppress embeds for the message.
    """

    if interaction.message:
        if interaction.response.is_done():
            return await interaction.followup.edit_message(
                interaction.message.id,
                content=content,
                embeds=embeds,
                embed=embed,
                file=file,
                files=files,
                attachments=attachments,
                view=view,
                allowed_mentions=allowed_mentions,
                thread=thread,
                suppress=suppress,
            )
        return await interaction.response.edit_message(
            content=content,
            embeds=embeds,
            embed=embed,
            file=file,
            files=files,
            attachments=attachments,
            view=view,
            allowed_mentions=allowed_mentions,
            suppress=suppress,
        )

    content_: str = content or MISSING
    embeds_: list[Embed] = embeds or MISSING
    embed_: Embed = embed or MISSING
    file_: File = file or MISSING
    files_: list[File] = files or MISSING
    view_: View = view or MISSING
    allowed_mentions_: AllowedMentions = allowed_mentions or MISSING
    thread_: Snowflake = thread or MISSING

    if interaction.response.is_done():
        return await interaction.followup.send(
            content=content_,
            embeds=embeds_,
            embed=embed_,
            file=file_,
            files=files_,
            view=view_,
            allowed_mentions=allowed_mentions_,
            thread=thread_,
        )
    return await interaction.response.send_message(
        content=content_,
        embeds=embeds_,
        embed=embed_,
        file=file_,
        files=files_,
        view=view_,
        allowed_mentions=allowed_mentions_,
    )
