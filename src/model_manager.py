from src.core.functions import get_fields
from src.core.observer.event_models import DeleteModelEvent, AddModelEvent, ModelOperationErrorEvent, \
    ModelOperationSuccessEvent, ChangeModelEvent
from src.core.observer.event_type import EventType
from src.core.observer.observer_service import ObserverService
from src.dto.abstract_dto import AbstractDto
from src.models.abstract_model import AbstractModel
from src.models.validators.exceptions import OperationException
from src.models.validators.functions import validate_val
from src.repository import RepoKeys, Repository

"""Класс для добавления, изменения и удаления объектов из репозитория"""
class ModelManager:

    """Метод для добавления новой модели в репозиторий"""
    @staticmethod
    def add_model(repo_key: str, model_type: type[AbstractModel], dto: AbstractDto, cache=None):
        repo = Repository()
        cache = cache or repo.get_all_models()
        model: AbstractModel = model_type.from_dto(dto, cache)
        key = RepoKeys(repo_key)
        repo.data[key][model.id] = model

        observer = ObserverService()
        observer.add(EventType.MODEL_ADD, model.on_add)
        observer.add(EventType.MODEL_DELETE, model.on_delete)
        observer.add(EventType.MODEL_CHANGE, model.on_change)

        observer.make_event(AddModelEvent.create(model))
        observer.make_event(ModelOperationSuccessEvent.create(f"Модель `{model.id}` успешно добавлена"))

        return model

    """Метод для изменения моделей"""
    @staticmethod
    def edit_model(
            model_type: AbstractModel,
            dto: AbstractDto
    ):
        model_id: str = dto.id
        repo = Repository()
        all_models = repo.get_all_models()

        if model_id not in all_models:
            raise OperationException(
                f"No model '{model_type.__name__}' with id: {model_id}"
            )
        model = all_models[model_id]
        validate_val(model, model_type)
        observer = ObserverService()

        try:
            observer.make_event(ChangeModelEvent.create(model))

            edited_model = model_type.from_dto(dto, all_models)
            for prop in get_fields(model):
                edited_value = getattr(edited_model, prop)
                if getattr(model, prop) != edited_value:
                    setattr(model, prop, edited_value)

            observer.make_event(ModelOperationSuccessEvent.create(f"Модель `{model_id}` успешно изменена"))
        except Exception as e:
            observer.make_event(ModelOperationErrorEvent.create(f"Ошибка при изменении модели с id `{model_id}`: {e}"))

        return model

    """Метод удаления модели по уникальному коду"""
    @staticmethod
    def delete_model(model_id: str):
        repo = Repository()

        observer = ObserverService()
        for key, models in repo.data.items():
            if model_id in repo.data[key]:
                model: AbstractModel = repo.data[key][model_id]
                try:
                    observer.make_event(DeleteModelEvent.create(model))
                    repo.data[key].pop(model_id)

                    observer.delete(EventType.MODEL_ADD, model.on_add)
                    observer.delete(EventType.MODEL_DELETE, model.on_delete)
                    observer.delete(EventType.MODEL_CHANGE, model.on_change)

                    observer.make_event(ModelOperationSuccessEvent.create(f"Модель `{model_id}` успешно удалена"))
                    return True
                except Exception as e:
                    observer.make_event(ModelOperationErrorEvent.create(f"Ошибка при удалении модели с id `{model_id}`: {e}"))
        return False


