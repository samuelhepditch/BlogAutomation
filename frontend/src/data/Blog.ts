import { BlogStatus } from "./BlogStatus";
import { RequestStatus } from "./RequestStatus";

class Blog {
    index: number;
    topic: string;
    keywords: string;
    requestStatus: RequestStatus;
    notes: string;
    status: BlogStatus;

    constructor(index: number, topic: string, keywords: string, requestStatus: RequestStatus, status: BlogStatus) {
        this.index = index;
        this.topic = topic;
        this.keywords = keywords;
        this.requestStatus = requestStatus;
        this.notes = "";
        this.status = status;
    }
}

export default Blog;