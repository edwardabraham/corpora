# -*- coding: utf-8 -*-

from .models import Sentence, Recording
from people.helpers import get_current_language

import logging
logger = logging.getLogger('corpora')

def get_sentence(request):
    current_language = get_current_language(request)
    logger.debug(current_language)
    if request.user.is_authenticated():
        recordings = Recording.objects.filter(person__user=request.user, sentence__language = current_language)
        logger.debug(recordings)
        sentences = Sentence.objects.filter(language=current_language).exclude(pk__in=[i.sentence.pk for i in recordings])
        logger.debug(sentences)
        return sentences.first()
    else:
        return get_sentence_annonymous(request)


def get_sentence_annonymous(request):

    sentences_without_recordings = Sentence.objects.filter(language=current_language, recording__is_null=True)
    logger.debug(sentences_without_recordings)
    return sentences_without_recordings.first()
