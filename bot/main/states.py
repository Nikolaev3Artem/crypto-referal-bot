from aiogram.dispatcher.filters.state import State, StatesGroup


class BlockchainSurvey(StatesGroup):
    address = State()
    confirmation = State()
    finishSurvey = State()