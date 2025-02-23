from typing import Callable
from my_reflex_app.components.navbar import navbar
from my_reflex_app.states.app_states import UserState
from my_reflex_app.pages.login import login_page

import reflex as rx

class PageState(rx.State):
    @rx.var(cache=False)
    async def is_logged_in(self) -> bool:
        user_state = await self.get_state(UserState)
        return user_state.is_logged_in


def template(
    page: Callable[[], rx.Component]
) -> rx.Component:
    return rx.cond(
        PageState.is_logged_in,
        rx.box(
            navbar(),
            rx.container(
                page(), 
                size="4"
                ),
            padding="16px",
        ),
        rx.box(
            rx.vstack(
            navbar(),
            login_page(),
            align="center"
            ),
            padding="16px",
        )
        
    )
