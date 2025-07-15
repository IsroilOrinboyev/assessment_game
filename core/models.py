import uuid
from django.db import models
from django.db.models import Avg, Sum

class Group(models.Model):
    """
    Represents a user-created group.
    """
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_group_score(self):
        """
        Sum of all scores received by all people in this group.
        """
        return self.people.aggregate(total=Sum('received_assessments__score'))['total'] or 0

    def average_group_score(self):
        """
        Average of all scores received by all people in this group.
        """
        return self.people.aggregate(avg=Avg('received_assessments__score'))['avg'] or 0


class Person(models.Model):
    """
    Member of a group who will assess and be assessed.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='people')
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nickname} ({self.group.name})"

    @property
    def total_score(self):
        """
        Total score received from all assessments.
        """
        return self.received_assessments.aggregate(total=Sum('score'))['total'] or 0

    @property
    def average_score(self):
        """
        Average score received from all assessments.
        """
        return self.received_assessments.aggregate(avg=Avg('score'))['avg'] or 0

    def rank_in_group(self):
        """
        Returns the person's rank (1-based) within their group based on total score.
        """
        people = list(self.group.people.all().annotate(score_sum=Sum('received_assessments__score')).order_by('-score_sum'))
        ranked_list = [p.id for p in people]
        return ranked_list.index(self.id) + 1 if self.id in ranked_list else None


class Question(models.Model):
    """
    Questions used for assessments.
    """
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Assessment(models.Model):
    """
    One score from one person to another on one question.
    """
    assessor = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='given_assessments')
    assessed = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='received_assessments')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assessor', 'assessed', 'question')

    def __str__(self):
        return f"{self.assessor.nickname} → {self.assessed.nickname}: {self.question.text} = {self.score}"

    def score_with_stars(self):
        """
        UI-friendly conversion of score to stars or emojis.
        """
        return "⭐" * self.score
