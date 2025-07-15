from django.db.models import Sum, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .models import Group, Person, Question, Assessment
from .forms import GroupForm, PersonForm, AssessmentForm, QuestionForm

def simple_mark(request):
    scores = range(1, 11)
    context = {
        'scores': scores,
    }
    return render(request, 'core/simple_mark.html', context)

# -----------------------------
# Group list (home page)
# -----------------------------
def group_list(request):
    groups = Group.objects.order_by('-created_at')
    return render(request, 'core/group_list.html', {'groups': groups})


# -----------------------------
# Create a new group
# -----------------------------
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' created successfully! 🎉")
            return redirect('core:group_list')
    else:
        form = GroupForm()
    return render(request, 'core/group_create.html', {'form': form})



def group_results(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Annotate people to get total and average in queryset (optional, but you already have properties)
    people = group.people.all()

    # Sort people using model property total_score
    sorted_people = sorted(people, key=lambda p: (-p.total_score, p.nickname))

    # Add rank and display attributes
    for idx, person in enumerate(sorted_people, start=1):
        person.rank = idx
        person.total_score_display = person.total_score
        person.average_score_display = round(person.average_score, 1)

    context = {
        'group': group,
        'people': sorted_people,
    }

    return render(request, 'core/results_page.html', context)



from django.http import JsonResponse

@csrf_exempt
def edit_member(request, group_id, member_id):
    person = get_object_or_404(Person, id=member_id, group__id=group_id)

    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        if nickname:
            person.nickname = nickname
            person.save()
            return JsonResponse({'success': True, 'nickname': nickname})
        return JsonResponse({'success': False, 'error': 'Nickname is required.'})

    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@csrf_exempt
def delete_member(request, group_id, member_id):
    person = get_object_or_404(Person, id=member_id, group__id=group_id)

    if request.method == 'POST':
        person.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@csrf_exempt
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        group.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@csrf_exempt
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            group.name = name
            group.save()
            return JsonResponse({'success': True, 'name': name})
        return JsonResponse({'success': False, 'error': 'Name is required.'})

    return JsonResponse({'success': False, 'error': 'Invalid request.'})


# -----------------------------
# Add member to a group
# -----------------------------
def add_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.group = group
            person.save()
            messages.success(request, f"Member '{person.nickname}' added to group '{group.name}'! ✅")
            return redirect('core:group_detail', group_id=group.id)
    else:
        form = PersonForm()
    return render(request, 'core/add_member.html', {'form': form, 'group': group})


# -----------------------------
# Group detail page
# -----------------------------
from django.db.models import Count

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    people = Person.objects.filter(group=group).order_by('nickname')

    questions = Question.objects.all().order_by('id')

    # Create default questions if none exist
    if not questions.exists():
        default_questions = [
            "How friendly is this person?",
            "How creative is this person?",
            "How reliable is this person?",
            "How supportive is this person?",
            "How funny is this person?",
            "How honest is this person?",
            "How confident is this person?",
            "How adaptable is this person?",
            "How empathetic is this person?",
            "How good is their leadership?"
        ]
        for text in default_questions:
            Question.objects.create(text=text)
        questions = Question.objects.all().order_by('id')

    first_question = questions.first()

    # Annotate each person to know if they finished assessing
    questions_count = questions.count()
    for person in people:
        expected_count = (people.count() - 1) * questions_count
        finished_count = person.given_assessments.count()
        person.finished_assessing = finished_count >= expected_count

    context = {
        'group': group,
        'people': people,
        'first_question': first_question,
    }
    return render(request, 'core/group_detail.html', context)



# -----------------------------
# Assessment page (one question)
# -----------------------------
def assessment_page(request, group_id, assessor_id, question_id):
    group = get_object_or_404(Group, id=group_id)
    assessor = get_object_or_404(Person, id=assessor_id)
    question = get_object_or_404(Question, id=question_id)

    # Targets: all people except the assessor
    targets = Person.objects.filter(group=group).exclude(id=assessor_id).order_by('nickname')

    if request.method == 'POST':
        for target in targets:
            score_value = request.POST.get(f'score_{target.id}')
            if score_value:
                score_value = int(score_value)
                assessment, created = Assessment.objects.get_or_create(
                    assessor=assessor,

                    assessed=target,
                    question=question,
                    defaults={'score': score_value}
                )
                if not created:
                    assessment.score = score_value
                    assessment.save()

        # Find next question
        questions = list(Question.objects.all().order_by('id'))
        current_index = questions.index(question)
        if current_index + 1 < len(questions):
            next_question = questions[current_index + 1]
            return redirect('core:assessment_page', group_id=group.id, assessor_id=assessor.id, question_id=next_question.id)
        else:
            messages.success(request, f"{assessor.nickname}'s assessments completed! ✅")
            return redirect('core:group_detail', group_id=group.id)

    context = {
        'group': group,
        'assessor': assessor,
        'question': question,
        'targets': targets,
    }
    return render(request, 'core/assessment_page.html', context)


# -----------------------------
# Add custom question
# -----------------------------
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New question added successfully! 📝")
            return redirect('core:group_list')
    else:
        form = QuestionForm()
    return render(request, 'core/add_question.html', {'form': form})
