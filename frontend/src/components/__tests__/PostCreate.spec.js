import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import PostCreate from '../PostCreate.vue';

describe('PostCreate.vue', () => {
  it('renders post create form', () => {
    const wrapper = mount(PostCreate);
    expect(wrapper.exists()).toBe(true);
  });
});
