
db = db.getSiblingDB('conversation');

db.createUser({
    user: "json_fay",
    pwd: "1qaz2wsx3edc$",
    roles:[
        {
            role: 'readWrite',
            db: 'conversation'

        },
    ],
});

db.createCollection('conversation_chunk_collection');


db.conversation_chunk_collection.insertMany({
    id: 'f524286b-a8a7-4c6a-90c7-3ede64af21db',
    conversationId: 'cbca95c4-0f16-4e02-8190-7689ec9e5c0e',
    noOfChunks: 0,
    createdAt: new Date('2023-10-01T00:00:00Z'),
    updatedAt: new Date('2023-10-01T00:00:00Z'),
    messages:[
        {
            id: 'f524286b-a8a7-4c6a-90c7-3ede64af21db',
            role: 'user',
            roleId: 'b768b11a-0550-4ba3-b479-b4ebc5fe0bfd',
            content: 'Hello, how are you?',
            referenceDocumentId: 'd0d31189-c325-4566-b1b4-59c5f5bd251f',
            createdAt: new Date('2023-10-01T00:00:00Z'),
            updatedAt: new Date('2023-10-01T00:00:00Z'),
            feedback: {
                rate: 0,
                comment: 'I am not satisfied with the response.'
            },    
            state: 'created',
        },
        {
            id: 'f524286b-a8a7-4c6a-90c7-3ede64af21dc',
            role: 'assistant',
            roleId: '2e5fadf5-19df-4209-9b22-dcc60ca478a8',
            referenceDocumentId: 'd0d31189-c325-4566-b1b4-59c5f5bd251f',
            content: 'I am fine, thank you! How can I assist you today?',
            createdAt: new Date('2023-10-01T00:00:00Z'),
            updatedAt: new Date('2023-10-01T00:00:00Z'),
            state: 'updated',
            feedback: null,
        }
    ]
});