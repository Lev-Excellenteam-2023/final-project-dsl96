import os
import file_db as db
import my_openai as ai
import asyncio

db = db.explainer_file_db()

already_processed_files_uid = set(db.get_all_dowload_uid())


async def explain_presentation(slides, name, uid):
    explain = await ai.async_get_explanation_to_presentation(slides, name)
    return {'uid': uid, 'explain': explain, 'name': name}


async def explain_new_presentation():
    all_upload_files_uid = db.get_all_upload_uid()

    tasks = []
    for uid in all_upload_files_uid:

        if uid in already_processed_files_uid:
            continue

        presentation = db.get_from_uploads(uid)

        # todo change topic to name
        tasks.append(explain_presentation(presentation['slides'], presentation['topic'], uid))

    explanations = await asyncio.gather(*tasks)

    for exp in explanations:
        db.save_to_download(exp['explain'], exp['uid'],exp['name'])
        print('explain' + exp['name'])


if __name__ == '__main__':
    asyncio.run(explain_new_presentation())
