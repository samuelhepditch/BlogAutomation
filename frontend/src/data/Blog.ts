import { BlogState } from "./BlogState";
import { RequestStatus } from "./RequestStatus";

class Blog {
    index: number;
    topic: string;
    keywords: string;
    status: RequestStatus;
    notes: string;
    state: BlogState;

    constructor(index: number, topic: string, keywords: string, status: RequestStatus, state: BlogState) {
        this.index = index;
        this.topic = topic;
        this.keywords = keywords;
        this.status = status;
        this.notes = "";
        this.state = state;
    }
}

export default Blog;